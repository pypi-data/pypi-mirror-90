#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Multibin Syntax

## Introduction

Many refinery units receive arguments which represent binary data, and usually these arguments can
be given in **multibin** format, which is a special syntax which allows to preprocess data with a
number of **handlers**. For example, the multibin expression `md5:password` preprocesses the
argument `password` (which is understood as its UTF8 encoding by default) using the `md5` handler,
which returns the MD5 hash of the input data. Consequently, the output of

    emit md5:password | hex -R

would be the string `5F4DCC3B5AA765D61D8327DEB882CF99`. The most important basic handlers to know
are:

- `s:string` disables all further preprocessing and interprets `string` as an UTF8 encoded string
- `u:string` same, but as an UTF16-LE encoded string
- `h:string` assumes that `string` is a hexadecimal string of even length and returns the decoded byte sequence.
- any unit's name can be prefixed to the string, i.e. `esc:\\n` corresponds to the line break character.

If a multibin argument does not use any handler, refinery first interprets the string as the path
of an existing file on disk and attempts to return the contents of this file. If this fails, the
UTF8 encoding of the string is returned.

The handlers `copy` and `cut` as well as their shortcuts `c` and `x` are **final** handlers like
the above example `s`, i.e. the string that follows `copy:` will not be interpreted as a multibin
expression. Indeed, `copy` and `cut` expect the remaining string to be in Python slice syntax. The
expression `copy:0:1` would, for example, represent the first byte of the input data. With `copy`,
this data is copied out of the input and used for the argument. With `cut`, this data is removed
from the input data and used for the argument. All `cut` operations are performed in the order in
which the arguments are specified on the command line. For example:
```
emit 1234 | cca x::1 x::1
```
will output the string `3412`.

The modifiers `s`, `u`, `h`, `copy` (or `c`), and `cut` (or `x`) along with using unit modifiers
should cover most use cases. To learn about other existing modifiers, refer to the rest of this
documentation.

## The Details

This module implements all argument parser types for the binary refinery. Notable classes for the
command line use are the following:

- `refinery.lib.argformats.DelayedBinaryArgument` (used almost everywhere)
- `refinery.lib.argformats.DelayedNumSeqArgument` (used by children of `refinery.units.blockwise.ArithmeticUnit`)
- `refinery.lib.argformats.DelayedRegexpArgument` (used by `refinery.rex`, `refinery.resub`)

All of the above classes inherit from `refinery.lib.argformats.DelayedArgument`. The following
mainly applies to `refinery.lib.argformats.DelayedBinaryArgument`, but the other two parsers work
similar. The classes implement the various modifiers which are available to multibin expressions.

The reason why these parsers have **"delayed"** in their name is that they allow the implementation
of handlers which require input data to be present, like the handlers `copy` and `cut`, which are
implemented in `refinery.lib.argformats.DelayedBinaryArgument.copy` and
`refinery.lib.argformats.DelayedBinaryArgument.cut`, respectively. These expressions can not be
evaluated immediately after the command line is parsed, but only as soon as input data becomes
available for processing.

In addition to the handlers which are implemented here, each refinery unit defines a (non-final)
modifier. For example, the expression `b64:Zm9v` corresponds to the binary string `foo`: The unit
`refinery.b64` is used to decode the string `Zm9v` here. Arguments can be passed to units in square
brackets and separated by commas, but there is no support for escaping comma characters. For
example, the multibin expression `xor[0xAA]:b64:2c/J2M/e` will return the binary string `secret` as
the final expression `2c/J2M/e` is base64-decoded and each byte xor'ed with the key `0xAA`. As a
second example, the expression

    hex[-R]:sha256:file:foobar.txt

will be parsed as the hexadecimal representation of the SHA256 hash of the file `foobar.txt`.
"""
import ast

from itertools import cycle, count, chain
from argparse import ArgumentTypeError
from contextlib import suppress
from functools import update_wrapper
from typing import Optional, Tuple, Union, Mapping, Any, List, TypeVar, Iterable, ByteString, Callable

from ..lib.frame import Chunk
from ..lib.tools import isbuffer
from ..lib.loader import resolve, EntryNotFound

FinalType = TypeVar('T')
DelayedType = Callable[[ByteString], FinalType]
MaybeDelayedType = Union[DelayedType, FinalType]


class ParserError(ArgumentTypeError): pass
class VariablesMissing(ParserError): pass


class PythonExpression:
    """
    Implements a parser for any Python expression with a prescribed set of variable
    names permitted to occur in the expression. The resulting object is a callable
    which can be given the string representation of such an expression. In turn, the
    result of this operation is either the value of the expression if no variables
    were present, or a callable which expects keyword arguments corresponding to the
    permitted variable names.
    """

    _ALLOWED_NODE_TYPES = {
        ast.Add,
        ast.BinOp,
        ast.BitAnd,
        ast.BitAnd,
        ast.BitOr,
        ast.BitXor,
        ast.BoolOp,
        ast.Compare,
        ast.Constant,
        ast.Div,
        ast.Eq,
        ast.FloorDiv,
        ast.Gt,
        ast.GtE,
        ast.IfExp,
        ast.Index,
        ast.Invert,
        ast.Is,
        ast.IsNot,
        ast.Load,
        ast.LShift,
        ast.Lt,
        ast.LtE,
        ast.List,
        ast.MatMult,
        ast.Mod,
        ast.Mult,
        ast.Name,
        ast.Not,
        ast.NotEq,
        ast.Num,
        ast.Or,
        ast.Pow,
        ast.RShift,
        ast.Slice,
        ast.Sub,
        ast.Subscript,
        ast.Tuple,
        ast.UAdd,
        ast.UnaryOp,
        ast.USub
    }

    def __init__(self, definition, *variables, constants=None, all_variables_allowed=False):
        constants = constants or {}
        variables = set(variables) | set(constants)
        try:
            expression = ast.parse(definition)
            nodes = ast.walk(expression)
        except Exception:
            raise ParserError(F'The provided expression could not be parsed: {definition!s}')
        if type(next(nodes)) != ast.Module:
            raise ParserError(F'unknown error parsing the expression: {definition!s}')
        if type(next(nodes)) != ast.Expr:
            raise ParserError(F'not a valid Python expression: {definition!s}')
        nodes = list(nodes)
        types = set(type(node) for node in nodes)
        names = set(node.id for node in nodes if type(node) == ast.Name)
        if not types <= self._ALLOWED_NODE_TYPES:
            raise ParserError(
                'the following operations are not allowed: {}'.format(
                    ', '.join(t.__name__ for t in types - self._ALLOWED_NODE_TYPES))
            )
        if not all_variables_allowed and not names <= variables:
            raise VariablesMissing(
                'the following variable names are unknown: {}'.format(
                    ', '.join(names - variables))
            )

        self.variables = names
        self.constants = constants
        self.definition = definition

    def __str__(self):
        return self.definition

    def __call__(self, **values):
        values.update(self.constants)
        for v in self.variables:
            if v not in values:
                raise ValueError(F'unbound variable {v}, cannot evaluate')
        return eval(self.definition, None, values)

    @classmethod
    def evaluate(cls, definition, **values):
        expression = cls(definition, *list(values))
        return expression(**values)


def sliceobj(expression: Union[int, str, slice], **variables) -> slice:
    """
    Uses `refinery.lib.argformats.PythonExpression` to parse slice expressions
    where the bounds can be given as arithmetic expressions. For example, this
    argument format type will process the string `0x11:0x11+4*0x34` as the slice
    object `slice(17, 225, None)`.
    """
    if isinstance(expression, slice):
        return expression
    if isinstance(expression, int):
        sliced = (expression,)
    else:
        sliced = expression.split(':')
        if not sliced or len(sliced) > 3:
            raise ArgumentTypeError(F'the expression {expression} is not a valid slice.')
        try:
            sliced = [None if not t else PythonExpression.evaluate(t, **variables) for t in sliced]
        except VariablesMissing:
            class SliceAgain(LazyEvaluation):
                def __call__(self, data): return sliceobj(expression, **data.meta)
            return SliceAgain()
    if len(sliced) == 1:
        k = sliced[0]
        return slice(k, k + 1) if k + 1 else slice(k, None, None)
    return slice(*sliced)


def utf8(x):
    """
    Returns the UTF8 encoding of the given string.
    """
    return x.encode('UTF8')


class IncompatibleHandler(ValueError):
    """
    This exception is generated when `refinery.lib.argformats.DelayedArgument` handlers
    are chained in an incompatible way.
    """
    def __init__(self, type_expected, type_observed, modifier):
        self.type_expected = type_expected
        self.type_observed = type_observed
        self.modifier = modifier
        modifier_name = F'handler {modifier}' if modifier else 'default handler'
        super().__init__('{} received {} but expected {}'.format(
            modifier_name,
            type_observed.__name__,
            type_expected.__name__
        ))


class TooLazy(Exception):
    """
    Exception which indicates that an argument parser requires input data before it can be
    evaluated.
    """
    pass


class VariableMissing(RuntimeError):
    def __init__(self, name):
        super().__init__(F'The variable {name} is not defined.')
        self.name = name


class LazyEvaluation:
    """
    Empty parent class for any unit that throws `refinery.lib.argformats.TooLazy`.
    """
    pass


class DelayedArgumentDispatch:
    """
    This class is used as a decorator for the default handler of classes that inherit from
    `refinery.lib.argformats.DelayedArgument`. After decorating the routine `handler` with
    `refinery.lib.argformats.DelayedArgumentDispatch`, `handler.register` can be used to
    register additional handlers.
    """
    class Wrapper:
        def can_handle(self, *a): return self.ego.can_handle(*a)
        def terminates(self, *a): return self.ego.terminates(*a)

        def __init__(self, ego, arg):
            self.ego = ego
            self.arg = arg

        def __call__(self, *args, **kwargs):
            return self.ego(self.arg, *args, **kwargs)

    def __init__(self, method):
        update_wrapper(self, method)
        self.default = method
        self.handlers = {}
        self.final = {}
        self.units = {}

    def _get_unit(self, name, *args):
        name = name.replace('-', '_')
        uhash = hash((name,) + args)
        if uhash in self.units:
            return self.units[uhash]
        try:
            unit = resolve(name)
        except EntryNotFound:
            return None
        else:
            unit = unit and unit.assemble(*args).detach()
            self.units[uhash] = unit
            return unit

    def __get__(self, instance, t=None):
        return self.Wrapper(self, instance)

    def __call__(self, instance, data, modifier=None, *args):
        try:
            handler = self.default if modifier is None else self.handlers[modifier]
            return handler(instance, data, *args)
        except KeyError:
            unit = self._get_unit(modifier, *args)
            if not unit:
                raise ArgumentTypeError(F'failed to build unit {modifier}')
            result = unit.act(data)
            return result if isbuffer(result) else B''.join(result)

    def can_handle(self, modifier, *args):
        return modifier in self.handlers or bool(self._get_unit(modifier, *args))

    def terminates(self, modifier):
        """
        Indicates whether the given registered modifier is final.
        """
        return self.final.get(modifier, False)

    def register(self, *modifiers, final=False):
        """
        Registers a new modifier handler.
        """
        def _register(method):
            for modifier in modifiers:
                self.handlers[modifier] = method
                self.final[modifier] = final
            return method
        return _register


class DelayedArgument(LazyEvaluation):
    """
    This base class for delayed argument parsers implements parsing
    expressions into supported modifiers.
    """
    _ARG_BEGIN_TOKEN = '['
    _ARG_CLOSE_TOKEN = ']'
    _ARG_SPLIT_TOKEN = ','

    def __init__(self, expression: str):
        self.modifiers = []
        self.finalized = False
        while not self.finalized:
            name, arguments, newexpr = self._split_modifier(expression)
            if not name or not self.handler.can_handle(name, *arguments):
                break
            self.modifiers.append((name, arguments))
            expression = newexpr
            if self.handler.terminates(name):
                self.finalized = True
        self.seed = expression
        self.modifiers.reverse()

    def _split_modifier(self, expression: str) -> Tuple[Optional[str], Tuple[str], str]:
        brackets = 0
        name = None
        argoffset = 0
        arguments = ()
        for k, character in enumerate(expression):
            if character == self._ARG_BEGIN_TOKEN:
                if not brackets:
                    if argoffset:
                        # This is the second time we encounter what appears to be an
                        # argument list, before the modifier has ended. This is not
                        # possible, and we decide to assume that no modifier was used.
                        break
                    name = expression[:k]
                    argoffset = k + 1
                brackets += 1
                continue
            if character == self._ARG_CLOSE_TOKEN:
                if brackets == 1:
                    arguments += expression[argoffset:k],
                elif not brackets:
                    if argoffset:
                        raise ArgumentTypeError(
                            F'Unable to parse {expression}, too many closing brackets.'
                        )
                    else:
                        break
                brackets -= 1
                continue
            if character == self._ARG_SPLIT_TOKEN:
                if brackets == 1:
                    arguments += expression[argoffset:k],
                    argoffset = k + 1
            if character == ':' and not brackets:
                if name is None:
                    name = expression[:k]
                return name, arguments, expression[k + 1:]
        return None, (), expression

    def __call__(self, data: Union[ByteString, Chunk, None] = None) -> bytes:
        arg = self.seed
        mod = iter(self.modifiers)
        if not self.finalized:
            mod = chain(((None, ()),), mod)
        for name, arguments in mod:
            if isbuffer(arg):
                arg = Chunk(arg)
                with suppress(AttributeError):
                    arg.meta.update(data.meta)
            try:
                arg = self.handler(arg, name, *arguments)
            except VariableMissing as v:
                if data is not None:
                    raise
                raise TooLazy from v
            except AttributeError as AE:
                raise ArgumentTypeError(F'failed to apply modifier {name} to incoming data: {AE}') from AE
            if callable(arg):
                if data is None:
                    raise TooLazy
                arg = arg(data)
        return arg

    def handler(self, expression: str):
        """
        This method is overwritten by children of `refinery.lib.argformats.DelayedArgument`
        to implement the default handler.
        """
        raise NotImplementedError


class DelayedBinaryArgument(DelayedArgument):

    @DelayedArgumentDispatch
    def handler(self, expr: str) -> bytes:
        try:
            return open(expr, 'rb').read()
        except Exception:
            pass
        return utf8(expr)

    @handler.register('s', final=True)
    def s(self, string: str) -> bytes:
        """
        The final modifier `s:string` returns the UTF-8 encoded representation of `string`.
        """
        return string.encode('UTF8')

    @handler.register('u', final=True)
    def u(self, string: str) -> bytes:
        """
        The final modifier `u:string` returns the UTF16 (little endian without BOM) encoded
        representation of `string`.
        """
        return string.encode('UTF-16LE')

    @handler.register('a', final=True)
    def a(self, string: str) -> bytes:
        """
        The final modifier `a:string` returns the latin-1 encoded representation of `string`.
        """
        return string.encode('LATIN-1')

    @handler.register('H', 'h', final=True)
    def h(self, string: str) -> bytes:
        """
        The final modifier `h:string` (or `H:string`) returns the hex decoding of `string`.
        """
        import base64
        return base64.b16decode(string, casefold=True)

    @handler.register('f', 'file', final=True)
    def file(self, path: str) -> bytes:
        """
        The final modifier `f:path` or `file:path` returns the contents of the file located
        at the given path.
        """
        return open(path, 'rb').read()

    @handler.register('range', final=True)
    def range(self, region: str) -> bytes:
        """
        Implements the final modifier `range:bounds` to generate a sequence of bytes, where
        `bounds` is parsed as a `refinery.lib.argformats.sliceobj` with one exception: If
        `bounds` is just a single integer, it is interpreted as the upper bound for a sequence
        of bytes starting at zero.
        """
        try:
            bounds = number(region)
            return bytearray(range(bounds))
        except (ValueError, ArgumentTypeError):
            pass
        bounds = sliceobj(region)
        if bounds.stop is None:
            raise ArgumentTypeError('cannot generate unbounded byte sequence.')
        return bytearray(range(bounds.start or 0, bounds.stop, bounds.step or 1))

    @handler.register('c', 'copy', final=True)
    def copy(self, region: str) -> bytes:
        """
        Implements the final modifier `c:region` or `copy:region`, where `region` is parsed
        as a `refinery.lib.argformats.sliceobj`. The result contains the corresponding slice
        of the input data.
        """
        if not region or region.lower() == 'all':
            region = ':'
        return lambda d: memoryview(d)[sliceobj(region, **d.meta)]

    @handler.register('x', 'cut', final=True)
    def cut(self, region: str) -> bytes:
        """
        `x:region` and `cut:region` work like `refinery.lib.argformats.DelayedBinaryArgument.copy`,
        but the corresponding bytes are also removed from the input data.
        """
        def extract(data: Union[bytearray, Chunk]):
            try:
                meta = data.meta
            except AttributeError:
                meta = {}
            bounds = sliceobj(region, **meta)
            result = bytearray(data[bounds])
            data[bounds] = []
            return result
        return extract

    def _interpret_variable(self, name: str, obj: Any):
        if isbuffer(obj) or isinstance(obj, (list, tuple, set, int)):
            return obj
        if isinstance(obj, str):
            return utf8(obj)
        raise ValueError(F'The meta variable {name} is of type {type(obj).__name__} and no conversion to bytes is known.')

    @handler.register('var', final=True)
    def var(self, name: str) -> bytes:
        """
        The final handler `var:name` contains the value of the meta variable `name`.
        The variable remains attached to the chunk.
        """
        def extract(data: Chunk):
            try:
                result = data.meta[name]
            except KeyError as K:
                raise VariableMissing(name) from K
            return self._interpret_variable(name, result)
        return extract

    @handler.register('xvar', final=True)
    def xvar(self, name: str) -> bytes:
        """
        The final handler `xvar:name` contains the value of the meta variable `name`.
        The variable is removed from the chunk and no longer available to subsequent
        units.
        """
        def extract(data: Chunk):
            try:
                result = data.meta.pop(name)
            except KeyError as K:
                raise VariableMissing(name) from K
            return self._interpret_variable(name, result)
        return extract


def multibin(expression: Union[str, bytes, bytearray]) -> Union[bytes, DelayedBinaryArgument]:
    """
    This is the argument parser type that uses `refinery.lib.argformats.DelayedBinaryArgument`.
    """
    if not isinstance(expression, str):
        return bytes(expression)
    arg = DelayedBinaryArgument(expression)
    with suppress(TooLazy):
        return arg()
    return arg


class DelayedNumSeqArgument(DelayedArgument):
    """
    A parser for sequences of numeric arguments. As `refinery.lib.argformats.DelayedNumSeqArgument.handler`
    uses `refinery.lib.argformats.multibin`, it is possible to use any handler specified in
    `refinery.lib.argformats.DelayedBinaryArgument` as long as these handlers precede any of the handlers
    defined here.
    """

    def _mbin(self, expr: str) -> bytes:
        binary = multibin(expr)
        if not binary:
            raise ArgumentTypeError('received empty binary argument')
        return binary

    def _iter(self, unknown):
        if hasattr(unknown, '__iter__'):
            it = list(unknown)
            if all(isinstance(t, int) for t in it):
                return it
        if isinstance(unknown, int):
            return (unknown,)
        raise ArgumentTypeError(
            F'numseq parser encountered {unknown} of type {type(unknown).__name__}, '
            F'but only integers are supported.'
        )

    @DelayedArgumentDispatch
    def handler(self, expression: str) -> Iterable[int]:
        """
        The default handler: Attempts to parse the input expression as a sequence of integers
        and uses `refinery.lib.argformats.multibin` to parse it if that fails.
        """
        try:
            return self._iter(PythonExpression.evaluate(expression))
        except Exception:
            return self._mbin(expression)

    @handler.register('e', 'eval')
    def ev(self, expression: Union[str, ByteString]) -> Iterable[int]:
        """
        Final modifier `e:expression` or `eval:expression`; uses a `refinery.lib.argformats.PythonExpression`
        parser to process expressions. The expression can contain any meta variable that is attached to the
        chunk. The `refinery.trivia` unit can be used to attach information such as chunk size and the chunk
        index within the current frame (see `refinery.lib.frame`).
        """
        if not isinstance(expression, str):
            try:
                expression = expression.decode('ascii')
            except AttributeError:
                return expression
        evaluator = PythonExpression(expression, all_variables_allowed=True)
        if evaluator.variables:
            def finalize(chunk):
                return self._iter(evaluator(**chunk.meta))
            return finalize
        return self._iter(evaluator())

    @handler.register('unpack', final=True)
    def unpack(self, expression: str, size=None) -> Iterable[int]:
        """
        Final modifier `unpack[size]:expression`; uses `refinery.lib.chunks.unpack` to
        convert a sequence of bytes into a sequence of numbers by unpacking them. The `expression`
        parameter is parsed with `refinery.lib.argformats.multibin` yielding this byte string.
        The optional parameter `size` has to be an integer expression whose absolute value gives
        the size of each encoded number in bytes. Its default value is `0`, which corresponds to
        choosing the size automatically in the following manner: If the length of the buffer is
        uneven, the value `1` is chosen. If the length modulo `4` is nonzero, the value `2` is
        chosen. If the length is divisible by `4`, then `4` is chosen.
        """
        from .chunks import unpack
        size = int(size, 0) if size else 0
        obig = size < 0
        size = abs(size)
        mbin = self._mbin(expression)
        if not callable(mbin) and size:
            return list(unpack(mbin, size, obig))
        def delayed(d): # noqa
            data = mbin(d) if callable(mbin) else mbin
            size = {1: 1, 2: 2, 3: 1, 0: 4}[len(data) % 4]
            return list(unpack(data, size, False))
        return delayed

    @handler.register('inc')
    def inc(self, it: Iterable[int], wrap=None) -> Iterable[int]:
        """
        The modifier `inc:it` or `inc[wrap]:it` expects a sequence `it` of integers
        (a binary string is interpreted as the sequence of its byte values), iterates it
        cyclically and perpetually adds an increasing counter to the result. If `wrap`
        is specified, then the counter is reduced modulo this number.
        """
        def delay(_):
            k = cycle(range(number(wrap))) if wrap else count()
            for item in cycle(it):
                yield item + next(k)
        return delay

    @handler.register('dec')
    def dec(self, it: Iterable[int], wrap=None) -> Iterable[int]:
        """
        Identical to `refinery.lib.argformats.DelayedNumSeqArgument.inc`, but the counter
        is subtracted from `it`.
        """
        def delay(_):
            k = cycle(range(number(wrap))) if wrap else count()
            for item in cycle(it):
                yield item - next(k)
        return delay


class DelayedRegexpArgument(DelayedArgument):
    """
    A parser for regular expressions arguments.
    """

    @DelayedArgumentDispatch
    def handler(self, expression: str) -> bytes:
        """
        The default handler encodes the input expression as latin-1 to return a binary
        string regular expression.
        Furthermore, the use of named patterns from `refinery.lib.patterns.formats` and
        `refinery.lib.patterns.indicators` is possible by means of the extension format
        `(??name)`. For example, the pattern `e:((??url)\\x00){4}` will match a sequence
        of four URL strings which are all terminated with a null character.
        """
        if '(??' in expression:
            import re
            from .patterns import formats, indicators

            def replace(match):
                name = match[1]
                return '(?:{})'.format(formats.get(
                    name, indicators.get(name, match[0])))

            expression = re.sub(
                R'\(\?\?({}|{})\)'.format(
                    '|'.join(p.name for p in formats),
                    '|'.join(p.name for p in indicators)
                ),
                replace,
                expression
            )

        return expression.encode('latin-1')

    @handler.register('yara')
    def yara(self, pattern: bytes) -> bytes:
        """
        The handler `yara:pattern` converts YARA syntax wildcard hexadecimal expressions
        into regular expressions. For example, `D?` is translated to `[\\xD0-\\xDF]`, the
        expression `[2-6]` becomes `.{2,6}`, and `?D` becomes the following substring:
        ```
        [\\x0D\\x1D\\x2D\\x3D\\x4D\\x5D\\x6D\\x7D\\x8D\\x9D\\xAD\\xBD\\xCD\\xDD\\xED\\xFD]
        ```
        Only two-letter hexadecimal sequences with optional `?` wildcards and wildcard
        ranges such as `[2-6]` are substituted, all other characters in the pattern are
        left unchanged.
        """
        import re

        def y2r(match):
            expr = match[0]
            if expr == B'??':
                return B'.'
            if B'?' not in expr:
                return BR'\x%s' % expr
            if expr.endswith(B'?'):
                return BR'[\x%c0-\x%cF]' % (expr[0], expr[0])
            return BR'[%s]' % BR''.join(
                BR'\x%x%c' % (k, expr[1]) for k in range(0x10)
            )

        def yara_range(rng):
            return B'.{%s}' % B','.join(t.strip() for t in rng[1:-1].split(B'-'))

        pattern = re.split(BR'(\[\s*\d+(?:\s*-\s*\d+)?\s*\])', pattern)
        pattern[0::2] = [re.sub(BR'[A-Fa-f0-9?]{2}', y2r, c) for c in pattern[::2]]
        pattern[1::2] = [yara_range(b) for b in pattern[1::2]]
        return B''.join(pattern)

    @handler.register('escape')
    def escape(self, str: bytes) -> bytes:
        """
        The handler `escape:str` returns a regular expression which matches the exact
        string sequence given by `str`, with special regular expression control characters
        escaped.
        """
        import re
        return re.escape(str)


class DelayedNumberArgument(DelayedArgument):
    """
    A parser for numeric arguments. As `refinery.lib.argformats.DelayedNumberArgument.handler`
    uses `refinery.lib.argformats.multibin`, it is possible to use any handler specified in
    `refinery.lib.argformats.DelayedBinaryArgument` as long as these handlers precede any of
    the handlers defined here.
    """
    def __init__(self, expression: str, min: int, max: int, bin: bool = False):
        self.min = min
        self.max = max
        self.bin = bin
        super().__init__(expression)

    def _mbin(self, converter: DelayedType[int], expr: str) -> MaybeDelayedType[int]:
        def bound_checked_converter(b: ByteString):
            value = converter(b)
            if self.min is not None and value < self.min or self.max is not None and value > self.max:
                a = '-∞' if self.min is None else self.min
                b = '∞' if self.max is None else self.max
                raise ValueError(F'value {value} is out of bounds [{a}, {b}]')
            return value
        binary = multibin(expr)
        if not binary:
            raise ArgumentTypeError('received empty binary argument')
        if callable(binary):
            return lambda d: bound_checked_converter(binary(d))
        return bound_checked_converter(binary)

    @DelayedArgumentDispatch
    def handler(self, expression: str) -> int:
        """
        The default handler: Attempts to parse the input expression as an integer.
        """
        def parse(b: Union[int, ByteString]) -> int:
            if isinstance(b, int):
                return b
            expression = PythonExpression(b.decode('utf8'))
            t = expression()
            if self.bin and not isinstance(t, int):
                raise ValueError(F'the expression with value {expression} is not an integer')
            return t
        return self._mbin(parse, expression)

    @handler.register('be', final=True)
    def be(self, expression: str) -> int:
        def be(b: ByteString): return int.from_bytes(b, 'big')
        return self._mbin(be, expression)

    @handler.register('le', final=True)
    def le(self, expression: str) -> int:
        def le(b: ByteString): return int.from_bytes(b, 'little')
        return self._mbin(le, expression)

    @handler.register('h', 'H', final=True)
    def hex(self, expression: str) -> int:
        return int(expression.upper().rstrip('H'), 16)


class number:
    __name__ = 'number'

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def __getitem__(self, bounds):
        return self.__class__(bounds.start, bounds.stop)

    def __call__(self, value):
        if isinstance(value, int):
            return value
        try:
            delay = DelayedNumberArgument(value, self.min, self.max)
            return delay()
        except TooLazy:
            return delay
        except ParserError:
            import re
            match = re.fullmatch('(?:0x)?([A-F0-9]+)H?', value, flags=re.IGNORECASE)
            if not match:
                raise
            return number(F'0x{match[1]}')


number = number()
"""
The singleton instance of a class that uses `refinery.lib.argformats.PythonExpression`
to parse expressions with integer value. This singleton can be slice accessed to
create new number parsers, e.g. `number[0:]` will refuse to parse negative integer
expressions.
"""


def numbin(expression: Union[int, str]) -> Union[ByteString, int, DelayedNumberArgument]:
    """
    An argument parser using `refinery.lib.argformats.DelayedNumberArgument` but also allowing
    binary arguments. The result is either a byte string or a number.
    """
    arg = DelayedNumberArgument(expression, None, None, True)
    with suppress(TooLazy): return arg()
    return arg


def numseq(expression: Union[int, str]) -> Union[Iterable[int], DelayedNumSeqArgument]:
    """
    This is the argument parser type that uses `refinery.lib.argformats.DelayedNumSeqArgument`.
    """
    if isinstance(expression, int):
        return (expression,)
    arg = DelayedNumSeqArgument(expression)
    with suppress(TooLazy):
        return arg()
    return arg


def regexp(expression: str) -> Union[int, bytes, DelayedRegexpArgument]:
    """
    This is the argument parser type that uses `refinery.lib.argformats.DelayedRegexpArgument`.
    """
    arg = DelayedRegexpArgument(expression)
    with suppress(TooLazy):
        return arg()
    return arg


def OptionFactory(options: Mapping[str, Any], ignorecase: bool = False):
    """
    The factory produces an argument parser type that accepts the keys of `options`
    as possible values and causes the parsed argument to contain the corresponding
    value from the `options` dictionary.
    """

    class Option():
        def __init__(self, name: str):
            if ignorecase and name not in options:
                needle = name.upper()
                for key in options:
                    if needle == key.upper():
                        name = key
                        break
            if name not in options:
                raise ValueError('The option %s is not one of these: %s' % (name, list(options)))
            self.mode = options[name]
            self.name = name

        def __eq__(self, other):
            return str(other) == self.name

        def __hash__(self):
            return hash(self.name)

        def __str__(self):
            return self.name

        def __repr__(self):
            return self.name

        @property
        def value(self):
            return self.mode

    return Option


def extract_options(symbols, prefix='MODE_', *exceptions):
    """
    A helper function to extract all numeric constants from modules that have a certain
    prefix. `refinery.units.crypto.cipher.StandardCipherUnit` uses this to extract the
    block cipher modes of operation from block cipher modules of the `pycryptodome` library.
    """
    candidates = {
        k[len(prefix):]: getattr(symbols, k, None)
        for k in dir(symbols) if k.startswith(prefix) and all(
            e not in k for e in exceptions
        )
    }
    return {k: v for k, v in candidates.items() if isinstance(v, int)}


def pending(argument: Union[Any, Iterable[Any]]) -> bool:
    """
    This function returns a boolean value which indicates whether the given
    argument is a `refinery.lib.argformats.LazyEvaluation`.
    """
    if isinstance(argument, (list, tuple)):
        return any(pending(x) for x in argument)
    return isinstance(argument, LazyEvaluation)


def manifest(argument: Union[Any, List[Any]], data: bytearray) -> Union[Any, List[Any]]:
    """
    Returns the manifestation of a `refinery.lib.argformats.LazyEvaluation`
    on the given data. This function can change the data.
    """
    if isinstance(argument, (list, tuple)):
        return [manifest(x, data) for x in argument]
    return argument(data) if isinstance(argument, LazyEvaluation) else argument

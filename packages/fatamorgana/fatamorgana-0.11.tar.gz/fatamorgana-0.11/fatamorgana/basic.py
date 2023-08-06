"""
This module contains all datatypes and parsing/writing functions for
 all abstractions below the 'record' or 'block' level.
"""
from typing import List, Tuple, Type, Union, Optional, Any, Sequence
from fractions import Fraction
from enum import Enum
import math
import struct
import io
import warnings

try:
    import numpy
    _USE_NUMPY = True
except ImportError:
    _USE_NUMPY = False


'''
    Type definitions
'''
real_t = Union[int, float, Fraction]
repetition_t = Union['ReuseRepetition', 'GridRepetition', 'ArbitraryRepetition']
property_value_t = Union[int, bytes, 'AString', 'NString', 'PropStringReference', float, Fraction]


class FatamorganaError(Exception):
    """
    Base exception for all errors Fatamorgana raises
    """
    pass


class EOFError(FatamorganaError):
    """
    Premature end of file, or file continues past expected end.
    """
    pass


class SignedError(FatamorganaError):
    """
    Signed number being written into an unsigned-only slot.
    """
    pass


class InvalidDataError(FatamorganaError):
    """
    Malformed data (either input or output).
    """
    pass


class InvalidRecordError(FatamorganaError):
    """
    Invalid file structure (got an unexpected record type).
    """
    pass

class UnfilledModalError(FatamorganaError):
    """
    Attempted to call .get_var(), but var() was None!
    """
    pass


class PathExtensionScheme(Enum):
    """
    Enum for path extension schemes
    """
    Flush = 1
    HalfWidth = 2
    Arbitrary = 3


'''
    Constants
'''
MAGIC_BYTES: bytes = b'%SEMI-OASIS\r\n'


'''
    Basic IO
'''
def _read(stream: io.BufferedIOBase, n: int) -> bytes:
    """
    Read n bytes from the stream.
    Raise an EOFError if there were not enough bytes in the stream.

    Args:
        stream: Stream to read from.
        n: Number of bytes to read.

    Returns:
        The bytes that were read.

    Raises:
        EOFError if not enough bytes could be read.
    """
    b = stream.read(n)
    if len(b) != n:
        raise EOFError('Unexpected EOF')
    return b


def read_byte(stream: io.BufferedIOBase) -> int:
    """
    Read a single byte and return it.

    Args:
        stream: Stream to read from.

    Returns:
        The byte that was read.
    """
    return _read(stream, 1)[0]


def write_byte(stream: io.BufferedIOBase, n: int) -> int:
    """
    Write a single byte to the stream.

    Args:
        stream: Stream to read from.

    Returns:
        The number of bytes writen (1).
    """
    return stream.write(bytes((n,)))


def _py_read_bool_byte(stream: io.BufferedIOBase) -> List[bool]:
    """
    Read a single byte from the stream, and interpret its bits as
      a list of 8 booleans.

    Args:
        stream: Stream to read from.

    Returns:
        A list of 8 booleans corresponding to the bits (MSB first).
    """
    byte = _read(stream, 1)[0]
    bits = [bool((byte >> i) & 0x01) for i in reversed(range(8))]
    return bits

def _py_write_bool_byte(stream: io.BufferedIOBase, bits: Tuple[Union[bool, int], ...]) -> int:
    """
    Pack 8 booleans into a byte, and write it to the stream.

    Args:
        stream: Stream to write to.
        bits: A list of 8 booleans corresponding to the bits (MSB first).

    Returns:
        Number of bytes written (1).

    Raises:
        InvalidDataError if didn't receive 8 bits.
    """
    if len(bits) != 8:
        raise InvalidDataError('write_bool_byte received {} bits, requires 8'.format(len(bits)))
    byte = 0
    for i, bit in enumerate(reversed(bits)):
        byte |= bit << i
    return stream.write(bytes((byte,)))


if _USE_NUMPY:
    def _np_read_bool_byte(stream: io.BufferedIOBase) -> List[bool]:
        """
        Read a single byte from the stream, and interpret its bits as
          a list of 8 booleans.

        Args:
            stream: Stream to read from.

        Returns:
            A list of 8 booleans corresponding to the bits (MSB first).
        """
        byte_arr = _read(stream, 1)
        return numpy.unpackbits(numpy.frombuffer(byte_arr, dtype=numpy.uint8))

    def _np_write_bool_byte(stream: io.BufferedIOBase, bits: Tuple[Union[bool, int], ...]) -> int:
        """
        Pack 8 booleans into a byte, and write it to the stream.

        Args:
            stream: Stream to write to.
            bits: A list of 8 booleans corresponding to the bits (MSB first).

        Returns:
            Number of bytes written (1).

        Raises:
            InvalidDataError if didn't receive 8 bits.
        """
        if len(bits) != 8:
            raise InvalidDataError('write_bool_byte received {} bits, requires 8'.format(len(bits)))
        return stream.write(numpy.packbits(bits)[0])

    read_bool_byte = _np_read_bool_byte
    write_bool_byte = _np_write_bool_byte
else:
    read_bool_byte = _py_read_bool_byte
    write_bool_byte = _py_write_bool_byte

def read_uint(stream: io.BufferedIOBase) -> int:
    """
    Read an unsigned integer from the stream.

    The format used is sometimes called a "varint":
        - MSB of each byte is set to 1, except for the final byte.
        - Remaining bits of each byte form the binary representation
            of the integer, but are stored _least significant group first_.

    Args:
        stream: Stream to read from.

    Returns:
        The integer's value.
    """
    result = 0
    i = 0
    byte = _read(stream, 1)[0]
    result |= byte & 0x7f
    while byte & 0x80:
        i += 1
        byte = _read(stream, 1)[0]
        result |= (byte & 0x7f) << (7 * i)
    return result


def write_uint(stream: io.BufferedIOBase, n: int) -> int:
    """
    Write an unsigned integer to the stream.
    See format details in `read_uint()`.

    Args:
        stream: Stream to write to.
        n: Value to write.

    Returns:
        The number of bytes written.

    Raises:
        SignedError: if `n` is negative.
    """
    if n < 0:
        raise SignedError('uint must be positive: {}'.format(n))

    current = n
    byte_list = []
    while True:
        byte = current & 0x7f
        current >>= 7
        if current != 0:
            byte |= 0x80
            byte_list.append(byte)
        else:
            byte_list.append(byte)
            break
    return stream.write(bytes(byte_list))


def decode_sint(uint: int) -> int:
    """
    Decode a signed integer from its unsigned form.

    The encoded form is sometimes called "zigzag" representation:
        - The LSB is treated as the sign bit
        - The remainder of the bits encodes the absolute value

    Args:
        uint: Unsigned integer to decode from.

    Returns:
        The decoded signed integer.
    """
    return (uint >> 1) * (1 - 2 * (0x01 & uint))


def encode_sint(sint: int) -> int:
    """
    Encode a signed integer into its corresponding unsigned integer form.
    See `decode_sint()` for format details.

    Args:
        int: The signed integer to encode.

    Returns:
        Unsigned integer encoding for the input.
    """
    return (abs(sint) << 1) | (sint < 0)


def read_sint(stream: io.BufferedIOBase) -> int:
    """
    Read a signed integer from the stream.
    See `decode_sint()` for format details.

    Args:
        stream: Stream to read from.

    Returns:
        The integer's value.
    """
    return decode_sint(read_uint(stream))


def write_sint(stream: io.BufferedIOBase, n: int) -> int:
    """
    Write a signed integer to the stream.
    See `decode_sint()` for format details.

    Args:
        stream: Stream to write to.
        n: Value to write.

    Returns:
        The number of bytes written.
    """
    return write_uint(stream, encode_sint(n))


def read_bstring(stream: io.BufferedIOBase) -> bytes:
    """
    Read a binary string from the stream.
    The format is:
    - length: uint
    - data: bytes

    Args:
        stream: Stream to read from.

    Returns:
        Bytes containing the binary string.
    """
    length = read_uint(stream)
    return _read(stream, length)


def write_bstring(stream: io.BufferedIOBase, bstring: bytes):
    """
    Write a binary string to the stream.
    See `read_bstring()` for format details.

    Args:
       stream: Stream to write to.
       bstring: Binary string to write.

    Returns:
        The number of bytes written.
    """
    write_uint(stream, len(bstring))
    return stream.write(bstring)


def read_ratio(stream: io.BufferedIOBase) -> Fraction:
    """
    Read a ratio (unsigned) from the stream.
    The format is:
    - numerator: uint
    - denominator: uint

    Args:
        stream: Stream to read from.

    Returns:
        Fraction object containing the read value.
    """
    numer = read_uint(stream)
    denom = read_uint(stream)
    return Fraction(numer, denom)


def write_ratio(stream: io.BufferedIOBase, r: Fraction) -> int:
    """
    Write an unsigned ratio to the stream.
    See `read_ratio()` for format details.

    Args:
        stream: Stream to write to.
        r: Ratio to write (`Fraction` object).

    Returns:
        The number of bytes written.

    Raises:
        SignedError: if r is negative.
    """
    if r < 0:
        raise SignedError('Ratio must be unsigned: {}'.format(r))
    size = write_uint(stream, r.numerator)
    size += write_uint(stream, r.denominator)
    return size


def read_float32(stream: io.BufferedIOBase) -> float:
    """
    Read a 32-bit float from the stream.

    Args:
        stream: Stream to read from.

    Returns:
        The value read.
    """
    b = _read(stream, 4)
    return struct.unpack("<f", b)[0]


def write_float32(stream: io.BufferedIOBase, f: float) -> int:
    """
    Write a 32-bit float to the stream.

    Arsg:
        stream: Stream to write to.
        f: Value to write.

    Returns:
        The number of bytes written (4).
    """
    b = struct.pack("<f", f)
    return stream.write(b)


def read_float64(stream: io.BufferedIOBase) -> float:
    """
    Read a 64-bit float from the stream.

    Args:
        stream: Stream to read from.

    Returns:
        The value read.
    """
    b = _read(stream, 8)
    return struct.unpack("<d", b)[0]


def write_float64(stream: io.BufferedIOBase, f: float) -> int:
    """
    Write a 64-bit float to the stream.

    Args:
        stream: Stream to write to.
        f: Value to write.

    Returns:
        The number of bytes written (8).
    """
    b = struct.pack("<d", f)
    return stream.write(b)


def read_real(stream: io.BufferedIOBase, real_type: int = None) -> real_t:
    """
    Read a real number from the stream.

    Format consists of a uint denoting the type, which can be passed
     as an argument or read from the stream (default), followed by the
     type-dependent value:

    0: uint (positive)
    1: uint (negative)
    2: uint (positive reciprocal, i.e. 1/u)
    3: uint (negative reciprocal, i.e. -1/u)
    4: ratio (positive)
    5: ratio (negative)
    6: 32-bit float
    7: 64-bit float

    Args:
        stream: Stream to read from.
        real_type: Type of real number to read. If `None` (default),
            the type is read from the stream.

    Returns:
        The value read.

    Raises:
        InvalidDataError: if real_type is invalid.
    """

    if real_type is None:
        real_type = read_uint(stream)
    if real_type == 0:
        return read_uint(stream)
    if real_type == 1:
        return -read_uint(stream)
    if real_type == 2:
        return Fraction(1, read_uint(stream))
    if real_type == 3:
        return Fraction(-1, read_uint(stream))
    if real_type == 4:
        return Fraction(read_uint(stream), read_uint(stream))
    if real_type == 5:
        return Fraction(-read_uint(stream), read_uint(stream))
    if real_type == 6:
        return read_float32(stream)
    if real_type == 7:
        return read_float64(stream)
    raise InvalidDataError('Invalid real type: {}'.format(real_type))


def write_real(stream: io.BufferedIOBase,
               r: real_t,
               force_float32: bool = False
               ) -> int:
    """
    Write a real number to the stream.
    See read_real() for format details.

    This function will store r as an int if it is already an int,
      but will not cast it into an int if it is an integer-valued
      float or Fraction.
    Since python has no 32-bit floats, the force_float32 parameter
      will perform the cast at write-time if set to True (default False).

    Args:
        stream: Stream to write to.
        r: Value to write.
        force_float32: If `True`, casts r to float32 when writing.
            Default `False`.

    Returns:
        The number of bytes written.
    """
    size = 0
    if isinstance(r, int):
        size += write_uint(stream, r < 0)
        size += write_uint(stream, abs(r))
    elif isinstance(r, Fraction):
        if abs(r.numerator) == 1:
            size += write_uint(stream, 2 + (r < 0))
            size += write_uint(stream, abs(r.denominator))
        else:
            size += write_uint(stream, 4 + (r < 0))
            size += write_ratio(stream, abs(r))
    elif isinstance(r, float):
        if force_float32:
            size += write_uint(stream, 6)
            size += write_float32(stream, r)
        else:
            size += write_uint(stream, 7)
            size += write_float64(stream, r)
    return size


class NString:
    """
    Class for handling "name strings", which hold one or more
      printable ASCII characters (0x21 to 0x7e, inclusive).

    `__init__` can be called with either a string or bytes object;
      subsequent reading/writing should use the `string` and
      `bytes` properties.
    """
    _string: str

    def __init__(self, string_or_bytes: Union[bytes, str]):
        """
        Args:
            string_or_bytes: Content of the `NString`.
        """
        if isinstance(string_or_bytes, str):
            self.string = string_or_bytes
        else:
            self.bytes = string_or_bytes

    @property
    def string(self) -> str:
        return self._string

    @string.setter
    def string(self, string: str):
        if len(string) == 0 or not all(0x21 <= ord(c) <= 0x7e for c in string):
            raise InvalidDataError('Invalid n-string {}'.format(string))
        self._string = string

    @property
    def bytes(self) -> bytes:
        return self._string.encode('ascii')

    @bytes.setter
    def bytes(self, bstring: bytes):
        if len(bstring) == 0 or not all(0x21 <= c <= 0x7e for c in bstring):
            raise InvalidDataError('Invalid n-string {!r}'.format(bstring))
        self._string = bstring.decode('ascii')

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'NString':
        """
        Create an NString object by reading a bstring from the provided stream.

        Args:
            stream: Stream to read from.

        Returns:
            Resulting NString.

        Raises:
            InvalidDataError
        """
        return NString(read_bstring(stream))

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write this NString to a stream.

        Args:
            stream: Stream to write to.

        Returns:
            Number of bytes written.
        """
        return write_bstring(stream, self.bytes)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.string == other.string

    def __repr__(self) -> str:
        return '[N]' + self._string

    def __str__(self) -> str:
        return self._string


def read_nstring(stream: io.BufferedIOBase) -> str:
    """
    Read a name string from the provided stream.
    See `NString` for constraints on name strings.

    Args:
        stream: Stream to read from.

    Returns:
        Resulting string.

    Raises:
        InvalidDataError
    """
    return NString.read(stream).string


def write_nstring(stream: io.BufferedIOBase, string: str) -> int:
    """
    Write a name string to a stream.
    See `NString` for constraints on name strings.

    Args:
        stream: Stream to write to.
        string: String to write.

    Returns:
        Number of bytes written.

    Raises:
        InvalidDataError
    """
    return NString(string).write(stream)


class AString:
    """
    Class for handling "ascii strings", which hold zero or more
      ASCII characters (0x20 to 0x7e, inclusive).

    `__init__` can be called with either a string or bytes object;
      subsequent reading/writing should use the `string` and
      `bytes` properties.
    """
    _string: str

    def __init__(self, string_or_bytes: Union[bytes, str]):
        """
        Args:
            string_or_bytes: Content of the AString.
        """
        if isinstance(string_or_bytes, str):
            self.string = string_or_bytes
        else:
            self.bytes = string_or_bytes

    @property
    def string(self) -> str:
        return self._string

    @string.setter
    def string(self, string: str):
        if not all(0x20 <= ord(c) <= 0x7e for c in string):
            raise InvalidDataError('Invalid a-string {}'.format(string))
        self._string = string

    @property
    def bytes(self) -> bytes:
        return self._string.encode('ascii')

    @bytes.setter
    def bytes(self, bstring: bytes):
        if not all(0x20 <= c <= 0x7e for c in bstring):
            raise InvalidDataError('Invalid a-string {!r}'.format(bstring))
        self._string = bstring.decode('ascii')

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'AString':
        """
        Create an `AString` object by reading a bstring from the provided stream.

        Args:
            stream: Stream to read from.

        Returns:
            Resulting `AString`.

        Raises:
            InvalidDataError
        """
        return AString(read_bstring(stream))

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write this `AString` to a stream.

        Args:
            stream: Stream to write to.

        Returns:
            Number of bytes written.
        """
        return write_bstring(stream, self.bytes)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.string == other.string

    def __repr__(self) -> str:
        return '[A]' + self._string

    def __str__(self) -> str:
        return self._string


def read_astring(stream: io.BufferedIOBase) -> str:
    """
    Read an ASCII string from the provided stream.
    See `AString` for constraints on ASCII strings.

    Args:
        stream: Stream to read from.

    Returns:
        Resulting string.

    Raises:
        InvalidDataError
    """
    return AString.read(stream).string


def write_astring(stream: io.BufferedIOBase, string: str) -> int:
    """
    Write an ASCII string to a stream.
    See AString for constraints on ASCII strings.

    Args:
        stream: Stream to write to.
        string: String to write.

    Returns:
        Number of bytes written.

    Raises:
        InvalidDataError
    """
    return AString(string).write(stream)


class ManhattanDelta:
    """
    Class representing an axis-aligned ("Manhattan") vector.

    Attributes:
        vertical (bool): `True` if aligned along y-axis
        value (int): signed length of the vector
    """
    vertical = None         # type: bool
    value = None            # type: int

    def __init__(self, x: int, y: int):
        """
        One of `x` or `y` _must_ be zero!

        Args:
            x: x-displacement
            y: y-displacement
        """
        x = int(x)
        y = int(y)
        if x != 0:
            if y != 0:
                raise InvalidDataError('Non-Manhattan ManhattanDelta ({}, {})'.format(x, y))
            self.vertical = False
            self.value = x
        else:
            self.vertical = True
            self.value = y

    def as_list(self) -> List[int]:
        """
        Return a list representation of this vector.

        Returns:
            `[x, y]`
        """
        xy = [0, 0]
        xy[self.vertical] = self.value
        return xy

    def as_uint(self) -> int:
        """
        Return this vector encoded as an unsigned integer.
        See `ManhattanDelta.from_uint()` for format details.

        Returns:
            uint encoding of this vector.
        """
        return (encode_sint(self.value) << 1) | self.vertical

    @staticmethod
    def from_uint(n: int) -> 'ManhattanDelta':
        """
        Construct a ManhattanDelta object from its unsigned integer encoding.

        The LSB of the encoded object is 1 if the vector is aligned to the
         y-axis, or 0 if aligned to the x-axis.
        The remaining bits are used to encode a signed integer containing
         the signed length of the vector (see `encode_sint()` for format details).

        Args:
            n: Unsigned integer representation of a `ManhattanDelta` vector.

        Returns:
            The `ManhattanDelta` object that was encoded by `n`.
        """
        d = ManhattanDelta(0, 0)
        d.value = decode_sint(n >> 1)
        d.vertical = bool(n & 0x01)
        return d

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'ManhattanDelta':
        """
        Read a `ManhattanDelta` object from the provided stream.

        See `ManhattanDelta.from_uint()` for format details.

        Args:
            stream: The stream to read from.

        Returns:
            The `ManhattanDelta` object that was read from the stream.
        """
        n = read_uint(stream)
        return ManhattanDelta.from_uint(n)

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write a `ManhattanDelta` object to the provided stream.

        See `ManhattanDelta.from_uint()` for format details.

        Args:
            stream: The stream to write to.

        Returns:
            The number of bytes written.
        """
        return write_uint(stream, self.as_uint())

    def __eq__(self, other: Any) -> bool:
        return hasattr(other, 'as_list') and self.as_list() == other.as_list()

    def __repr__(self) -> str:
        return '{}'.format(self.as_list())


class OctangularDelta:
    """
    Class representing an axis-aligned or 45-degree ("Octangular") vector.

    Attributes:
        proj_mag (int): projection of the vector onto the x or y axis (non-zero)
        octangle (int): bitfield:
            bit 2: 1 if non-axis-aligned (non-Manhattan)
            if Manhattan:
                bit 1: 1 if direction is negative
                bit 0: 1 if direction is y
            if non-Manhattan:
                bit 1: 1 if in lower half-plane
                bit 0: 1 if x==-y

            Resulting directions:
                0: +x, 1: +y, 2: -x, 3: -y,
                4: +x+y, 5: -x+y,
                6: +x-y, 7: -x-y
    """
    proj_mag: int
    octangle: int

    def __init__(self, x: int, y: int):
        """
        Either `abs(x)==abs(y)`, `x==0`, or `y==0` _must_ be true!

        Args:
            x: x-displacement
            y: y-displacement
        """
        x = int(x)
        y = int(y)
        if x == 0 or y == 0:
            axis = (y != 0)
            val = x | y
            sign = val < 0
            self.proj_mag = abs(val)
            self.octangle = (sign << 1) | axis
        elif abs(x) == abs(y):
            xn = (x < 0)
            yn = (y < 0)
            self.proj_mag = abs(x)
            self.octangle = (1 << 2) | (yn << 1) | (xn != yn)
        else:
            raise InvalidDataError('Non-octangular delta! ({}, {})'.format(x, y))

    def as_list(self) -> List[int]:
        """
        Return a list representation of this vector.

        Returns:
            `[x, y]`
        """
        if self.octangle < 4:
            xy = [0, 0]
            axis = self.octangle & 0x01 > 0
            sign = self.octangle & 0x02 > 0
            xy[axis] = self.proj_mag * (1 - 2 * sign)
            return xy
        else:
            yn = (self.octangle & 0x02) > 0
            xyn = (self.octangle & 0x01) > 0
            ys = 1 - 2 * yn
            xs = ys * (1 - 2 * xyn)
            v = self.proj_mag
            return [v * xs, v * ys]

    def as_uint(self) -> int:
        """
        Return this vector encoded as an unsigned integer.
        See `OctangularDelta.from_uint()` for format details.

        Returns:
            uint encoding of this vector.
        """
        return (self.proj_mag << 3) | self.octangle

    @staticmethod
    def from_uint(n: int) -> 'OctangularDelta':
        """
        Construct an `OctangularDelta` object from its unsigned integer encoding.

        The low 3 bits are equal to `proj_mag`, as specified in the class
         docstring.
        The remaining bits are used to encode an unsigned integer containing
         the length of the vector.

        Args:
            n: Unsigned integer representation of an `OctangularDelta` vector.

        Returns:
            The `OctangularDelta` object that was encoded by `n`.
        """
        d = OctangularDelta(0, 0)
        d.proj_mag = n >> 3
        d.octangle = n & 0b0111
        return d

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'OctangularDelta':
        """
        Read an `OctangularDelta` object from the provided stream.

        See `OctangularDelta.from_uint()` for format details.

        Args:
            stream: The stream to read from.

        Returns:
            The `OctangularDelta` object that was read from the stream.
        """
        n = read_uint(stream)
        return OctangularDelta.from_uint(n)

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write an `OctangularDelta` object to the provided stream.

        See `OctangularDelta.from_uint()` for format details.

        Args:
            stream: The stream to write to.

        Returns:
            The number of bytes written.
        """
        return write_uint(stream, self.as_uint())

    def __eq__(self, other: Any) -> bool:
        return hasattr(other, 'as_list') and self.as_list() == other.as_list()

    def __repr__(self) -> str:
        return '{}'.format(self.as_list())


class Delta:
    """
    Class representing an arbitrary vector

    Attributes
        x (int): x-displacement
        y (int): y-displacement
    """
    x: int
    y: int

    def __init__(self, x: int, y: int):
        """
        Args:
            x: x-displacement
            y: y-displacement
        """
        x = int(x)
        y = int(y)
        self.x = x
        self.y = y

    def as_list(self) -> List[int]:
        """
        Return a list representation of this vector.

        Returns:
            `[x, y]`
        """
        return [self.x, self.y]

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'Delta':
        """
        Read a `Delta` object from the provided stream.

        The format consists of one or two unsigned integers.
        The LSB of the first integer is 1 if a second integer is present.
        If two integers are present, the remaining bits of the first
         integer are an encoded signed integer (see `encode_sint()`), and
         the second integer is an encoded signed_integer.
        Otherwise, the remaining bits of the first integer are an encoded
         `OctangularData` (see `OctangularData.from_uint()`).

        Args:
            stream: The stream to read from.

        Returns:
            The `Delta` object that was read from the stream.
        """
        n = read_uint(stream)
        if (n & 0x01) == 0:
            x, y = OctangularDelta.from_uint(n >> 1).as_list()
        else:
            x = decode_sint(n >> 1)
            y = read_sint(stream)
        return Delta(x, y)

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write a `Delta` object to the provided stream.

        See `Delta.from_uint()` for format details.

        Args:
            stream: The stream to write to.

        Returns:
            The number of bytes written.
        """
        if self.x == 0 or self.y == 0 or abs(self.x) == abs(self.y):
            return write_uint(stream, OctangularDelta(self.x, self.y).as_uint() << 1)
        else:
            size = write_uint(stream, (encode_sint(self.x) << 1) | 0x01)
            size += write_uint(stream, encode_sint(self.y))
            return size

    def __eq__(self, other: Any) -> bool:
        return hasattr(other, 'as_list') and self.as_list() == other.as_list()

    def __repr__(self) -> str:
        return '{}'.format(self.as_list())


def read_repetition(stream: io.BufferedIOBase) -> repetition_t:
    """
    Read a repetition entry from the given stream.

    Args:
        stream: Stream to read from.

    Returns:
        The repetition entry.

    Raises:
        InvalidDataError: if an unexpected repetition type is read
    """
    rtype = read_uint(stream)
    if rtype == 0:
        return ReuseRepetition.read(stream, rtype)
    elif rtype in (1, 2, 3, 8, 9):
        return GridRepetition.read(stream, rtype)
    elif rtype in (4, 5, 6, 7, 10, 11):
        return ArbitraryRepetition.read(stream, rtype)
    else:
        raise InvalidDataError('Unexpected repetition type: {}'.format(rtype))


def write_repetition(stream: io.BufferedIOBase, repetition: repetition_t) -> int:
    """
    Write a repetition entry to the given stream.

    Args:
        stream: Stream to write to.
        repetition: The repetition entry to write.

    Returns:
        The number of bytes written.
    """
    return repetition.write(stream)


class ReuseRepetition:
    """
    Class representing a "reuse" repetition entry, which indicates that
     the most recently written repetition should be reused.
    """
    @staticmethod
    def read(_stream: io.BufferedIOBase, _repetition_type: int) -> 'ReuseRepetition':
        return ReuseRepetition()

    def write(self, stream: io.BufferedIOBase) -> int:
        return write_uint(stream, 0)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReuseRepetition)

    def __repr__(self) -> str:
        return 'ReuseRepetition'


class GridRepetition:
    """
    Class representing a repetition entry denoting a 1D or 2D array
     of regularly-spaced elements. The spacings are stored as one or
     two lattice vectors, and the extent of the grid is stored as the
     number of elements along each lattice vector.

    Attributes:
        a_vector (Tuple[int, int]): `(xa, ya)` vector specifying a center-to-center
                        displacement between adjacent elements in the grid.
        b_vector (Optional[Tuple[int, int]]): `(xb, yb)`, a second displacement,
                        present if a 2D grid is being specified.
        a_count (int): number of elements (>=1) along the grid axis specified by
                        `a_vector`.
        b_count (Optional[int]): Number of elements (>=1) along the grid axis
                        specified by `b_vector`, if `b_vector` is not `None`.
    """
    a_vector: List[int]
    b_vector: Optional[List[int]] = None
    a_count: int
    b_count: Optional[int] = None

    def __init__(self,
                 a_vector: List[int],
                 a_count: int,
                 b_vector: Optional[List[int]] = None,
                 b_count: Optional[int] = None):
        """
        Args:
            a_vector: First lattice vector, of the form `[x, y]`.
                Specifies center-to-center spacing between adjacent elements.
            a_count: Number of elements in the a_vector direction.
            b_vector: Second lattice vector, of the form `[x, y]`.
                Specifies center-to-center spacing between adjacent elements.
                Can be omitted when specifying a 1D array.
            b_count: Number of elements in the `b_vector` direction.
                Should be omitted if `b_vector` was omitted.

        Raises:
            InvalidDataError: if `b_count` and `b_vector` inputs conflict
                with each other or if `a_count < 1`.
        """
        if b_vector is None or b_count is None:
            if b_vector is not None or b_count is not None:
                raise InvalidDataError('Repetition has only one of'
                                       'b_vector and b_count')
        else:
            if b_count < 1:
                raise InvalidDataError('Repetition has too-small b_count')
            if b_count < 2:
                b_count = None
                b_vector = None
                warnings.warn('Removed b_count and b_vector since b_count == 1')

        if a_count < 2:
            raise InvalidDataError('Repetition has too-small a_count: '
                                   '{}'.format(a_count))
        self.a_vector = a_vector
        self.b_vector = b_vector
        self.a_count = a_count
        self.b_count = b_count

    @staticmethod
    def read(stream: io.BufferedIOBase, repetition_type: int) -> 'GridRepetition':
        """
        Read a `GridRepetition` from a stream.

        Args:
            stream: Stream to read from.
            repetition_type: Repetition type as defined in OASIS repetition spec.
                Valid types are 1, 2, 3, 8, 9.

        Returns:
            `GridRepetition` object read from stream.

        Raises:
            InvalidDataError: if `repetition_type` is invalid.
        """
        nb: Optional[int]
        b_vector: Optional[List[int]]
        if repetition_type == 1:
            na = read_uint(stream) + 2
            nb = read_uint(stream) + 2
            a_vector = [read_uint(stream), 0]
            b_vector = [0, read_uint(stream)]
        elif repetition_type == 2:
            na = read_uint(stream) + 2
            nb = None
            a_vector = [read_uint(stream), 0]
            b_vector = None
        elif repetition_type == 3:
            na = read_uint(stream) + 2
            nb = None
            a_vector = [0, read_uint(stream)]
            b_vector = None
        elif repetition_type == 8:
            na = read_uint(stream) + 2
            nb = read_uint(stream) + 2
            a_vector = Delta.read(stream).as_list()
            b_vector = Delta.read(stream).as_list()
        elif repetition_type == 9:
            na = read_uint(stream) + 2
            nb = None
            a_vector = Delta.read(stream).as_list()
            b_vector = None
        else:
            raise InvalidDataError('Invalid type for grid repetition '
                                   '{}'.format(repetition_type))
        return GridRepetition(a_vector, na, b_vector, nb)

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write the `GridRepetition` to a stream.

        A minimal representation is written (e.g., if `b_count==1`,
         a 1D grid is written)

        Args:
            stream: Stream to write to.

        Returns:
            Number of bytes written.

        Raises:
            InvalidDataError: if repetition is malformed.
        """
        if self.b_vector is None or self.b_count is None:
            if self.b_vector is not None or self.b_count is not None:
                raise InvalidDataError('Malformed repetition {}'.format(self))

            if self.a_vector[1] == 0:
                size = write_uint(stream, 2)
                size += write_uint(stream, self.a_count - 2)
                size += write_uint(stream, self.a_vector[0])
            elif self.a_vector[0] == 0:
                size = write_uint(stream, 3)
                size += write_uint(stream, self.a_count - 2)
                size += write_uint(stream, self.a_vector[1])
            else:
                size = write_uint(stream, 9)
                size += write_uint(stream, self.a_count - 2)
                size += Delta(*self.a_vector).write(stream)
        else:
            if self.a_vector[1] == 0 and self.b_vector[0] == 0:
                size = write_uint(stream, 1)
                size += write_uint(stream, self.a_count - 2)
                size += write_uint(stream, self.b_count - 2)
                size += write_uint(stream, self.a_vector[0])
                size += write_uint(stream, self.b_vector[1])
            elif self.a_vector[0] == 0 and self.b_vector[1] == 0:
                size = write_uint(stream, 1)
                size += write_uint(stream, self.b_count - 2)
                size += write_uint(stream, self.a_count - 2)
                size += write_uint(stream, self.b_vector[0])
                size += write_uint(stream, self.a_vector[1])
            else:
                size = write_uint(stream, 8)
                size += write_uint(stream, self.a_count - 2)
                size += write_uint(stream, self.b_count - 2)
                size += Delta(*self.a_vector).write(stream)
                size += Delta(*self.b_vector).write(stream)
        return size

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self.a_count != other.a_count or self.b_count != other.b_count:
            return False
        if any(self.a_vector[ii] != other.a_vector[ii] for ii in range(2)):
            return False
        if self.b_vector is None and other.b_vector is None:
            return True
        if self.b_vector is None or other.b_vector is None:
            return False
        if any(self.b_vector[ii] != other.b_vector[ii] for ii in range(2)):
            return False
        return True

    def __repr__(self) -> str:
        return 'GridRepetition: ({} : {} |  {} : {})'.format(self.a_count, self.a_vector,
                                                             self.b_count, self.b_vector)


class ArbitraryRepetition:
    """
    Class representing a repetition entry denoting a 1D or 2D array
     of arbitrarily-spaced elements.

    Attributes:
        x_displacements (List[int]): x-displacements between consecutive elements
        y_displacements (List[int]): y-displacements between consecutive elements
    """

    x_displacements: List[int]
    y_displacements: List[int]

    def __init__(self,
                 x_displacements: List[int],
                 y_displacements: List[int]):
        """
        Args:
            x_displacements: x-displacements between consecutive elements
            y_displacements: y-displacements between consecutive elements
        """
        self.x_displacements = x_displacements
        self.y_displacements = y_displacements

    @staticmethod
    def read(stream: io.BufferedIOBase, repetition_type: int) -> 'ArbitraryRepetition':
        """
        Read an `ArbitraryRepetition` from a stream.

        Args:
            stream: Stream to read from.
            repetition_type: Repetition type as defined in OASIS repetition spec.
                Valid types are 4, 5, 6, 7, 10, 11.

        Returns:
            `ArbitraryRepetition` object read from stream.

        Raises:
            InvalidDataError: if `repetition_type` is invalid.
        """
        if repetition_type == 4:
            n = read_uint(stream) + 1
            x_displacements = [read_uint(stream) for _ in range(n)]
            y_displacements = [0] * len(x_displacements)
        elif repetition_type == 5:
            n = read_uint(stream) + 1
            mult = read_uint(stream)
            x_displacements = [mult * read_uint(stream) for _ in range(n)]
            y_displacements = [0] * len(x_displacements)
        elif repetition_type == 6:
            n = read_uint(stream) + 1
            y_displacements = [read_uint(stream) for _ in range(n)]
            x_displacements = [0] * len(y_displacements)
        elif repetition_type == 7:
            n = read_uint(stream) + 1
            mult = read_uint(stream)
            y_displacements = [mult * read_uint(stream) for _ in range(n)]
            x_displacements = [0] * len(y_displacements)
        elif repetition_type == 10:
            n = read_uint(stream) + 1
            x_displacements = []
            y_displacements = []
            for _ in range(n):
                x, y = Delta.read(stream).as_list()
                x_displacements.append(x)
                y_displacements.append(y)
        elif repetition_type == 11:
            n = read_uint(stream) + 1
            mult = read_uint(stream)
            x_displacements = []
            y_displacements = []
            for _ in range(n):
                x, y = Delta.read(stream).as_list()
                x_displacements.append(x * mult)
                y_displacements.append(y * mult)
        else:
            raise InvalidDataError('Invalid ArbitraryRepetition repetition_type: {}'.format(repetition_type))
        return ArbitraryRepetition(x_displacements, y_displacements)

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write the `ArbitraryRepetition` to a stream.

        A minimal representation is attempted; common factors in the
         displacements will be factored out, and lists of zeroes will
         be omitted.

        Args:
            stream: Stream to write to.

        Returns:
            Number of bytes written.
        """
        def get_gcd(vals: List[int]) -> int:
            """
            Get the greatest common denominator of a list of ints.
            """
            if len(vals) == 1:
                return vals[0]

            greatest = vals[0]
            for v in vals[1:]:
                greatest = math.gcd(greatest, v)
                if greatest == 1:
                    break
            return greatest

        x_gcd = get_gcd(self.x_displacements)
        y_gcd = get_gcd(self.y_displacements)
        if y_gcd == 0:
            if x_gcd <= 1:
                size = write_uint(stream, 4)
                size += write_uint(stream, len(self.x_displacements) - 1)
                size += sum(write_uint(stream, d) for d in self.x_displacements)
            else:
                size = write_uint(stream, 5)
                size += write_uint(stream, len(self.x_displacements) - 1)
                size += write_uint(stream, x_gcd)
                size += sum(write_uint(stream, d // x_gcd) for d in self.x_displacements)
        elif x_gcd == 0:
            if y_gcd <= 1:
                size = write_uint(stream, 6)
                size += write_uint(stream, len(self.y_displacements) - 1)
                size += sum(write_uint(stream, d) for d in self.y_displacements)
            else:
                size = write_uint(stream, 7)
                size += write_uint(stream, len(self.y_displacements) - 1)
                size += write_uint(stream, y_gcd)
                size += sum(write_uint(stream, d // y_gcd) for d in self.y_displacements)
        else:
            gcd = math.gcd(x_gcd, y_gcd)
            if gcd <= 1:
                size = write_uint(stream, 10)
                size += write_uint(stream, len(self.x_displacements) - 1)
                size += sum(Delta(x, y).write(stream)
                            for x, y in zip(self.x_displacements, self.y_displacements))
            else:
                size = write_uint(stream, 11)
                size += write_uint(stream, len(self.x_displacements) - 1)
                size += write_uint(stream, gcd)
                size += sum(Delta(x // gcd, y // gcd).write(stream)
                            for x, y in zip(self.x_displacements, self.y_displacements))
        return size

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, type(self))
                and self.x_displacements == other.x_displacements
                and self.y_displacements == other.y_displacements)

    def __repr__(self) -> str:
        return 'ArbitraryRepetition: x{} y{})'.format(self.x_displacements, self.y_displacements)


def read_point_list(stream: io.BufferedIOBase) -> List[List[int]]:
    """
    Read a point list from a stream.

    Args:
        stream: Stream to read from.

    Returns:
        Point list of the form `[[x0, y0], [x1, y1], ...]`

    Raises:
        InvalidDataError: if an invalid list type is read.
    """
    list_type = read_uint(stream)
    list_len = read_uint(stream)
    if list_type == 0:
        points = []
        dx, dy = 0, 0
        for i in range(list_len):
            point = [0, 0]
            n = read_sint(stream)
            if n == 0:
                raise InvalidDataError('Zero-sized 1-delta')
            point[i % 2] = n
            points.append(point)
            if i % 2:
                dy += n
            else:
                dx += n
        points.append([-dx, 0])
        points.append([0, -dy])
    elif list_type == 1:
        points = []
        dx, dy = 0, 0
        for i in range(list_len):
            point = [0, 0]
            n = read_sint(stream)
            if n == 0:
                raise Exception('Zero-sized 1-delta')
            point[(i + 1) % 2] = n
            points.append(point)
            if i % 2:
                dx += n
            else:
                dy += n
        points.append([0, -dy])
        points.append([-dx, 0])
    elif list_type == 2:
        points = [ManhattanDelta.read(stream).as_list() for _ in range(list_len)]
    elif list_type == 3:
        points = [OctangularDelta.read(stream).as_list() for _ in range(list_len)]
    elif list_type == 4:
        points = [Delta.read(stream).as_list() for _ in range(list_len)]
    elif list_type == 5:
        deltas = [Delta.read(stream).as_list() for _ in range(list_len)]
        if _USE_NUMPY:
            points = numpy.cumsum(deltas, axis=0)
        else:
            points = []
            x = 0
            y = 0
            for delta in deltas:
                x += delta[0]
                y += delta[1]
                points.append([x, y])
    else:
        raise InvalidDataError('Invalid point list type')
    return points


def write_point_list(stream: io.BufferedIOBase,
                     points: List[Sequence[int]],
                     fast: bool = False,
                     implicit_closed: bool = True
                     ) -> int:
    """
    Write a point list to a stream.

    Args:
        stream: Stream to write to.
        points: List of points, of the form `[[x0, y0], [x1, y1], ...]`
        fast: If `True`, avoid searching for a compact representation for
            the point list.
        implicit_closed: Set to True if the list represents an implicitly
            closed polygon, i.e. there is an implied line segment from `points[-1]`
            to `points[0]`. If False, such segments are ignored, which can result in
            a more compact representation for non-closed paths (e.g. a Manhattan
            path with non-colinear endpoints). If unsure, use the default.
            Default `True`.

    Returns:
        Number of bytes written.
    """
    # If we're in a hurry, just write the points as arbitrary Deltas
    if fast:
        size = write_uint(stream, 4)
        size += write_uint(stream, len(points))
        size += sum(Delta(x, y).write(stream) for x, y in points)
        return size

    # If Manhattan with alternating direction,
    #  set one of h_first or v_first to True
    #  otherwise both end up False
    previous = points[0]
    h_first = previous[1] == 0 and len(points) % 2 == 0
    v_first = previous[0] == 0 and len(points) % 2 == 0
    for i, point in enumerate(points[1:]):
        if (h_first and i % 2 == 0) or (v_first and i % 2 == 1):
            if point[0] != previous[0] or point[1] == previous[1]:
                h_first = False
                v_first = False
                break
        else:
            if point[1] != previous[1] or point[0] == previous[0]:
                h_first = False
                v_first = False
                break
        previous = point

    # If one of h_first or v_first, write a bunch of 1-deltas
    if h_first:
        size = write_uint(stream, 0)
        size += write_uint(stream, len(points))
        size += sum(write_sint(stream, x + y) for x, y in points)
        return size
    elif v_first:
        size = write_uint(stream, 1)
        size += write_uint(stream, len(points))
        size += sum(write_sint(stream, x + y) for x, y in points)
        return size

    # Try writing a bunch of Manhattan or Octangular deltas
    deltas: Union[List[ManhattanDelta], List[OctangularDelta], List[Delta]]
    list_type = None
    try:
        deltas = [ManhattanDelta(x, y) for x, y in points]
        if implicit_closed:
            ManhattanDelta(points[-1][0] - points[0][0], points[-1][1] - points[0][1])
        list_type = 2
    except:
        try:
            deltas = [OctangularDelta(x, y) for x, y in points]
            if implicit_closed:
                OctangularDelta(points[-1][0] - points[0][0], points[-1][1] - points[0][1])
            list_type = 3
        except:
            pass
    if list_type is not None:
        size = write_uint(stream, list_type)
        size += write_uint(stream, len(points))
        size += sum(d.write(stream) for d in deltas)
        return size

    '''
    Looks like we need to write arbitrary deltas,
     so we should check if it's better to write plain deltas,
     or change-in-deltas.
    '''
    # If it improves by decision_factor, use change-in-deltas
    decision_factor = 4
    if _USE_NUMPY:
        arr = numpy.array(points)
        diff = numpy.diff(arr, axis=0)
        if arr[1, :].sum() < diff.sum() * decision_factor:
            list_type = 4
            deltas = [Delta(x, y) for x, y in points]
        else:
            list_type = 5
            deltas = [Delta(*points[0])] + [Delta(x, y) for x, y in diff]
    else:
        previous = [0, 0]
        diff = []
        for point in points:
            d = [point[0] - previous[0],
                 point[1] - previous[1]]
            previous = point
            diff.append(d)

        if sum(sum(p) for p in points) < sum(sum(d) for d in diff) * decision_factor:
            list_type = 4
            deltas = [Delta(x, y) for x, y in points]
        else:
            list_type = 5
            deltas = [Delta(x, y) for x, y in diff]

    size = write_uint(stream, list_type)
    size += write_uint(stream, len(points))
    size += sum(d.write(stream) for d in deltas)
    return size


class PropStringReference:
    """
    Reference to a property string.

    Attributes:
        ref (int): ID of the target
        ref_type (Type): Type of the target: `bytes`, `NString`, or `AString`
    """
    ref: int
    reference_type: Type

    def __init__(self, ref: int, ref_type: Type):
        """
        :param ref: ID number of the target.
        :param ref_type: Type of the target. One of bytes, NString, AString.
        """
        self.ref = ref
        self.ref_type = ref_type

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.ref == other.ref and self.reference_type == other.reference_type

    def __repr__(self) -> str:
        return '[{} : {}]'.format(self.ref_type, self.ref)


def read_property_value(stream: io.BufferedIOBase) -> property_value_t:
    """
    Read a property value from a stream.

    The property value consists of a type (unsigned integer) and type-
     dependent data.

    Data types:
    0...7:  real number; property value type is reused for real number type
    8: unsigned integer
    9: signed integer
    10: ASCII string (`AString`)
    11: binary string (`bytes`)
    12: name string (`NString`)
    13: `PropStringReference` to `AString`
    14: `PropStringReference` to `bstring` (i.e., to `bytes`)
    15: `PropStringReference` to `NString`

    Args:
        stream: Stream to read from.

    Returns:
        Value of the property, depending on type.

    Raises:
        InvalidDataError: if an invalid type is read.
    """
    ref_type: Type
    prop_type = read_uint(stream)
    if 0 <= prop_type <= 7:
        return read_real(stream, prop_type)
    elif prop_type == 8:
        return read_uint(stream)
    elif prop_type == 9:
        return read_sint(stream)
    elif prop_type == 10:
        return AString.read(stream)
    elif prop_type == 11:
        return read_bstring(stream)
    elif prop_type == 12:
        return NString.read(stream)
    elif prop_type == 13:
        ref_type = AString
        ref = read_uint(stream)
        return PropStringReference(ref, ref_type)
    elif prop_type == 14:
        ref_type = bytes
        ref = read_uint(stream)
        return PropStringReference(ref, ref_type)
    elif prop_type == 15:
        ref_type = NString
        ref = read_uint(stream)
        return PropStringReference(ref, ref_type)
    else:
        raise InvalidDataError('Invalid property type: {}'.format(prop_type))


def write_property_value(stream: io.BufferedIOBase,
                         value: property_value_t,
                         force_real: bool = False,
                         force_signed_int: bool = False,
                         force_float32: bool = False
                         ) -> int:
    """
    Write a property value to a stream.

    See `read_property_value()` for format details.

    Args:
        stream: Stream to write to.
        value: Property value to write. Can be an integer, a real number,
            `bytes` (`bstring`), `NString`, `AString`, or a `PropstringReference`.
        force_real: If `True` and value is an integer, writes an integer-
            valued real number instead of a plain integer. Default `False`.
        force_signed_int: If `True` and value is a positive integer,
            writes a signed integer. Default `False`.
        force_float32: If `True` and value is a float, writes a 32-bit
            float (real number) instead of a 64-bit float.

    Returns:
        Number of bytes written.
    """
    if isinstance(value, int) and not force_real:
        if force_signed_int or value < 0:
            size = write_uint(stream, 9)
            size += write_sint(stream, value)
        else:
            size = write_uint(stream, 8)
            size += write_uint(stream, value)
    elif isinstance(value, (Fraction, float, int)):
        size = write_real(stream, value, force_float32)
    elif isinstance(value, AString):
        size = write_uint(stream, 10)
        size += value.write(stream)
    elif isinstance(value, bytes):
        size = write_uint(stream, 11)
        size += write_bstring(stream, value)
    elif isinstance(value, NString):
        size = write_uint(stream, 12)
        size += value.write(stream)
    elif isinstance(value, PropStringReference):
        if value.ref_type == AString:
            size = write_uint(stream, 13)
        elif value.ref_type == bytes:
            size = write_uint(stream, 14)
        if value.ref_type == AString:
            size = write_uint(stream, 15)
        size += write_uint(stream, value.ref)
    else:
        raise Exception('Invalid property type: {} ({})'.format(type(value), value))
    return size


def read_interval(stream: io.BufferedIOBase) -> Tuple[Optional[int], Optional[int]]:
    """
    Read an interval from a stream.
    These are used for storing layer info.

    The format consists of a type specifier (unsigned integer) and
     a variable number of integers:
    type 0: 0, inf (no data)
    type 1: 0, b   (unsigned integer b)
    type 2: a, inf (unsigned integer a)
    type 3: a, a   (unsigned integer a)
    type 4: a, b   (unsigned integers a, b)

    Args:
        stream: Stream to read from.

    Returns:
        `(lower, upper)`, where
        `lower` can be `None` if there is an implicit lower bound of `0`
        `upper` can be `None` if there is no upper bound (`inf`)

    Raises:
        InvalidDataError: On malformed data.
    """
    interval_type = read_uint(stream)
    if interval_type == 0:
        return None, None
    elif interval_type == 1:
        return None, read_uint(stream)
    elif interval_type == 2:
        return read_uint(stream), None
    elif interval_type == 3:
        v = read_uint(stream)
        return v, v
    elif interval_type == 4:
        return read_uint(stream), read_uint(stream)
    else:
        raise InvalidDataError('Unrecognized interval type: {}'.format(interval_type))


def write_interval(stream: io.BufferedIOBase,
                   min_bound: Optional[int] = None,
                   max_bound: Optional[int] = None
                   ) -> int:
    """
    Write an interval to a stream.
    Used for layer data; see `read_interval()` for format details.

    Args:
        stream: Stream to write to.
        min_bound: Lower bound on the interval, can be None (implicit 0, default)
        max_bound: Upper bound on the interval, can be None (unbounded, default)

    Returns:
        Number of bytes written.
    """
    if min_bound is None:
        if max_bound is None:
            return write_uint(stream, 0)
        else:
            return write_uint(stream, 1) + write_uint(stream, max_bound)
    else:
        if max_bound is None:
            return write_uint(stream, 2) + write_uint(stream, min_bound)
        elif min_bound == max_bound:
            return write_uint(stream, 3) + write_uint(stream, min_bound)
        else:
            size = write_uint(stream, 4)
            size += write_uint(stream, min_bound)
            size += write_uint(stream, max_bound)
            return size


class OffsetEntry:
    """
    Entry for the file's offset table.

    Attributes:
        strict (bool): If `False`, the records pointed to by this
            offset entry may also appear elsewhere in the file. If `True`, all
            records of the type pointed to by this offset entry must be present
            in a contiuous block at the specified offset [pad records also allowed].
            Additionally:
            - All references to strict-mode records must be
                explicit (using reference_number).
            - The offset may point to an encapsulating CBlock record, if the first
                record in that CBlock is of the target record type. A strict modei
                table cannot begin in the middle of a CBlock.
        offset (int): offset from the start of the file; may be 0
                for records that are not present.
    """
    strict: bool = False
    offset: int = 0

    def __init__(self, strict: bool = False, offset: int = 0):
        """
        Args:
            strict: `True` if the records referenced are written in
                strict mode (see class docstring). Default `False`.
            offset: Offset from the start of the file for the
                referenced records; may be `0` if records are absent.
                Default `0`.
        """
        self.strict = strict
        self.offset = offset

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'OffsetEntry':
        """
        Read an offset entry from a stream.

        Args:
            stream: Stream to read from.

        Returns:
            Offset entry that was read.
        """
        entry = OffsetEntry()
        entry.strict = read_uint(stream) > 0
        entry.offset = read_uint(stream)
        return entry

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write this offset entry to a stream.

        Args:
            stream: Stream to write to.

        Returns:
            Number of bytes written
        """
        return write_uint(stream, self.strict) + write_uint(stream, self.offset)

    def __repr__(self) -> str:
        return 'Offset(s: {}, o: {})'.format(self.strict, self.offset)


class OffsetTable:
    """
    Offset table, containing OffsetEntry data for each of 6 different
    record types,

    CellName
    TextString
    PropName
    PropString
    LayerName
    XName

    which are stored in the above order in the file's offset table.

    Attributes:
        cellnames (OffsetEntry): Offset for CellNames
        textstrings (OffsetEntry): Offset for TextStrings
        propnames (OffsetEntry): Offset for PropNames
        propstrings (OffsetEntry): Offset for PropStrings
        layernames (OffsetEntry): Offset for LayerNames
        xnames (OffsetEntry): Offset for XNames
    """
    cellnames:   OffsetEntry
    textstrings: OffsetEntry
    propnames:   OffsetEntry
    propstrings: OffsetEntry
    layernames:  OffsetEntry
    xnames:      OffsetEntry

    def __init__(self,
                 cellnames: Optional[OffsetEntry] = None,
                 textstrings: Optional[OffsetEntry] = None,
                 propnames: Optional[OffsetEntry] = None,
                 propstrings: Optional[OffsetEntry] = None,
                 layernames: Optional[OffsetEntry] = None,
                 xnames: Optional[OffsetEntry] = None):
        """
        All parameters default to a non-strict entry with offset `0`.

        Args:
            cellnames: `OffsetEntry` for `CellName` records.
            textstrings: `OffsetEntry` for `TextString` records.
            propnames: `OffsetEntry` for `PropName` records.
            propstrings: `OffsetEntry` for `PropString` records.
            layernames: `OffsetEntry` for `LayerName` records.
            xnames: `OffsetEntry` for `XName` records.
        """
        if cellnames is None:
            cellnames = OffsetEntry()
        if textstrings is None:
            textstrings = OffsetEntry()
        if propnames is None:
            propnames = OffsetEntry()
        if propstrings is None:
            propstrings = OffsetEntry()
        if layernames is None:
            layernames = OffsetEntry()
        if xnames is None:
            xnames = OffsetEntry()

        self.cellnames = cellnames
        self.textstrings = textstrings
        self.propnames = propnames
        self.propstrings = propstrings
        self.layernames = layernames
        self.xnames = xnames

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'OffsetTable':
        """
        Read an offset table from a stream.
        See class docstring for format details.

        Args:
            stream: Stream to read from.

        Returns:
            The offset table that was read.
        """
        table = OffsetTable()
        table.cellnames = OffsetEntry.read(stream)
        table.textstrings = OffsetEntry.read(stream)
        table.propnames = OffsetEntry.read(stream)
        table.propstrings = OffsetEntry.read(stream)
        table.layernames = OffsetEntry.read(stream)
        table.xnames = OffsetEntry.read(stream)
        return table

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write this offset table to a stream.
        See class docstring for format details.

        Args:
            stream: Stream to write to.

        Returns:
            Number of bytes written.
        """
        size = self.cellnames.write(stream)
        size += self.textstrings.write(stream)
        size += self.propnames.write(stream)
        size += self.propstrings.write(stream)
        size += self.layernames.write(stream)
        size += self.xnames.write(stream)
        return size

    def __repr__(self) -> str:
        return 'OffsetTable({})'.format([self.cellnames, self.textstrings, self.propnames,
                                         self.propstrings, self.layernames, self.xnames])


def read_u32(stream: io.BufferedIOBase) -> int:
    """
    Read a 32-bit unsigned integer (little endian) from a stream.

    Args:
        stream: Stream to read from.

    Returns:
        The integer that was read.
    """
    b = _read(stream, 4)
    return struct.unpack('<I', b)[0]


def write_u32(stream: io.BufferedIOBase, n: int) -> int:
    """
    Write a 32-bit unsigned integer (little endian) to a stream.

    Args:
        stream: Stream to write to.
        n: Integer to write.

    Returns:
        The number of bytes written (4).

    Raises:
        SignedError: if `n` is negative.
    """
    if n < 0:
        raise SignedError('Negative u32: {}'.format(n))
    return stream.write(struct.pack('<I', n))


class Validation:
    """
    Validation entry, containing checksum info for the file.
    Format is a (standard) unsigned integer (checksum_type), possitbly followed
      by a 32-bit unsigned integer (checksum).

    The checksum is calculated using the entire file, excluding the final 4 bytes
      (the value of the checksum itself).

    Attributes:
        checksum_type (int): `0` for no checksum, `1` for crc32, `2` for checksum32
        checksum (Optional[int]): value of the checksum
    """
    checksum_type: int
    checksum: Optional[int] = None

    def __init__(self, checksum_type: int, checksum: int = None):
        """
        Args:
            checksum_type: 0,1,2 (No checksum, crc32, checksum32)
            checksum: Value of the checksum, or None.

        Raises:
            InvalidDataError: if `checksum_type` is invalid, or
                unexpected `checksum` is present.
        """
        if checksum_type < 0 or checksum_type > 2:
            raise InvalidDataError('Invalid validation type')
        if checksum_type == 0 and checksum is not None:
            raise InvalidDataError('Validation type 0 shouldn\'t have a checksum')
        self.checksum_type = checksum_type
        self.checksum = checksum

    @staticmethod
    def read(stream: io.BufferedIOBase) -> 'Validation':
        """
        Read a validation entry from a stream.
        See class docstring for format details.

        Args:
            stream: Stream to read from.

        Returns:
            The validation entry that was read.

        Raises:
            InvalidDataError: if an invalid validation type was encountered.
        """
        checksum_type = read_uint(stream)
        if checksum_type == 0:
            checksum = None
        elif checksum_type == 1:
            checksum = read_u32(stream)
        elif checksum_type == 2:
            checksum = read_u32(stream)
        else:
            raise InvalidDataError('Invalid validation type!')
        return Validation(checksum_type, checksum)

    def write(self, stream: io.BufferedIOBase) -> int:
        """
        Write this validation entry to a stream.
        See class docstring for format details.

        Args:
            stream: Stream to write to.

        Returns:
            Number of bytes written.

        Raises:
            InvalidDataError: if the checksum type can't be handled.
        """
        if self.checksum_type == 0:
            return write_uint(stream, 0)
        elif self.checksum is None:
            raise InvalidDataError('Checksum is empty but type is '
                                   '{}'.format(self.checksum_type))
        elif self.checksum_type == 1:
            return write_uint(stream, 1) + write_u32(stream, self.checksum)
        elif self.checksum_type == 2:
            return write_uint(stream, 2) + write_u32(stream, self.checksum)
        else:
            raise InvalidDataError('Unrecognized checksum type: '
                                   '{}'.format(self.checksum_type))

    def __repr__(self) -> str:
        return 'Validation(type: {} sum: {})'.format(self.checksum_type, self.checksum)


def write_magic_bytes(stream: io.BufferedIOBase) -> int:
    """
    Write the magic byte sequence to a stream.

    Args:
        stream: Stream to write to.

    Returns:
        Number of bytes written.
    """
    return stream.write(MAGIC_BYTES)


def read_magic_bytes(stream: io.BufferedIOBase):
    """
    Read the magic byte sequence from a stream.
    Raise an `InvalidDataError` if it was not found.

    Args:
        stream: Stream to read from.

    Raises:
        InvalidDataError: if the sequence was not found.
    """
    magic = _read(stream, len(MAGIC_BYTES))
    if magic != MAGIC_BYTES:
        raise InvalidDataError('Could not read magic bytes, '
                               'found {!r} : {}'.format(magic, magic.decode()))

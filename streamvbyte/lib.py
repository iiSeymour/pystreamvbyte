"""
Python bindings for libstreamvbyte
"""

import os
import sys
import ctypes
from functools import wraps

import numpy as np
from numba import vectorize, int16, int32, int8, uint16, uint32


if sys.platform.startswith("linux"):
    lib_ext = "so.0.0.1"
elif sys.platform == "darwin":
    lib_ext = "dylib"
else:
    raise Exception("Unsupported platform %s" % sys.platform)

location = os.environ.get("LIBSTREAMVBYTE", "./src/libstreamvbyte.%s" % lib_ext)
streamvbyte_lib = ctypes.cdll.LoadLibrary(location)

_encode = streamvbyte_lib.streamvbyte_encode
_encode.argtypes = (ctypes.POINTER(ctypes.c_uint32), ctypes.c_int, ctypes.POINTER(ctypes.c_uint8))
_encode.restype = ctypes.c_int

_decode = streamvbyte_lib.streamvbyte_decode
_decode.argtypes = (ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint32), ctypes.c_int)
_decode.restype = ctypes.c_int

_encode_0124 = streamvbyte_lib.streamvbyte_encode_0124
_encode_0124.argtypes = _encode.argtypes
_encode_0124.restype = _encode.restype

_decode_0124 = streamvbyte_lib.streamvbyte_decode_0124
_decode_0124.argtypes = _decode.argtypes
_decode_0124.restype = _decode.restype

_encode_delta = streamvbyte_lib.streamvbyte_delta_encode
_encode_delta.argtypes = _encode.argtypes + (ctypes.c_uint32,)
_encode_delta.restype = ctypes.c_int

_decode_delta = streamvbyte_lib.streamvbyte_delta_decode
_decode_delta.argtypes = _decode.argtypes + (ctypes.c_uint32,)
_decode_delta.restype = ctypes.c_int


@vectorize([uint32(int16, int8), uint32(int32, int8)])
def to_zig_zag(data, shift):
    return (data << 1) ^ (data >> shift)


@vectorize([uint32(uint32), uint16(uint32)])
def from_zig_zag(data):
    return (data >> 1) ^ (-(data & 1))


def max_compressed_bytes(length):
    """
    return the maximum number of compressed bytes given length input integers
    """
    cb = int((length + 3) / 4)
    db = length * 4
    return cb + db


def encode_factory(c_func):
    """
    Encode an array of a given length read from in to bout in varint format.
    Returns the number of bytes written.
    The number of values being stored (length) is not encoded in the compressed stream,
    the caller is responsible for keeping a record of this length.
    The pointer "in" should point to "length" values of size uint32_t
    there is no alignment requirement on the out pointer
    For safety, the out pointer should point to at least streamvbyte_max_compressedbyte(length)
    bytes.
    Uses 1,2,3 or 4 bytes per value + the decoding keys
    """
    @wraps(c_func)
    def encode(data, prev=0):

        if np.issubdtype(data.dtype, np.signedinteger):
            diffs = np.ediff1d(data, to_begin=data[0])
            shift = np.int8(data.dtype.itemsize * 8 - 1)
            data = to_zig_zag(diffs, shift)

        if np.issubdtype(data.dtype, np.uint16):
            data = data.astype(np.uint32)

        output = np.zeros(max_compressed_bytes(len(data)), dtype=np.uint8)
        encoded_size = c_func(
            data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),
            len(data),
            output.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
            prev
        )
        return output[:encoded_size]
    return encode


def decode_factory(c_func):
    """
    Read "length" 32-bit integers in varint format from in, storing the result in out.
    Returns the number of bytes read.
    The caller is responsible for knowing how many integers ("length") are to be read:
    this information ought to be stored somehow.
    There is no alignment requirement on the "in" pointer.
    The out pointer should point to length * sizeof(uint32_t) bytes.
    """
    @wraps(c_func)
    def decode(data, n, prev=0, dtype=None):

        output = np.zeros(n, dtype=np.uint32)
        c_func(
            data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
            output.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),
            n,
            prev,
        )

        if dtype and np.issubdtype(dtype, np.signedinteger):
            zigzag = from_zig_zag(output)
            output = np.cumsum(zigzag, dtype=dtype)
        elif dtype and output.dtype != dtype:
            return output.astype(dtype)
        return output

    return decode


encode = encode_factory(_encode)
encode_0124 = encode_factory(_encode_0124)
encode_delta = encode_factory(_encode_delta)
decode = decode_factory(_decode)
decode_0124 = decode_factory(_decode_0124)
decode_delta = decode_factory(_decode_delta)

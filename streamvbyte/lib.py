"""
Python bindings for libstreamvbyte
"""

from functools import wraps

import numpy as np

from _streamvbyte import lib, ffi


def max_compressed_bytes(length):
    """
    return the maximum number of compressed bytes given length input integers
    """
    cb = int((length + 3) / 4)
    db = length * 4
    return cb + db


def encode_factory(c_func, prev=None):

    @wraps(c_func)
    def encode(data):
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
        # cast up int16 types
        if data.dtype == np.int16: data = data.astype(np.int32)
        elif data.dtype == np.uint16: data = data.astype(np.uint32)

        length = len(data)

        # delta zigzag encode signed types
        if data.dtype == np.int32:
            udata = np.empty(len(data), dtype=np.uint32)
            u = ffi.cast("uint32_t *", ffi.from_buffer(udata))
            d = ffi.cast("int32_t *", ffi.from_buffer(data))
            lib.zigzag_delta_encode(d, u, length, 0)
            data = udata

        n = max_compressed_bytes(length)
        output = np.empty(n, dtype=np.uint8)

        d = ffi.cast("uint32_t *", ffi.from_buffer(data))
        o = ffi.cast("uint8_t *", ffi.from_buffer(output))

        if prev is None:
            encoded_size = c_func(d, length, o)
        else:
            encoded_size = c_func(d, length, o, prev)

        return output[:encoded_size]

    return encode


def decode_factory(c_func, prev=None):
    @wraps(c_func)
    def decode(data, n, dtype=None):
        """
        Read "length" 32-bit integers in varint format from in, storing the result in out.
        Returns the number of bytes read.
        The caller is responsible for knowing how many integers ("length") are to be read:
        this information ought to be stored somehow.
        There is no alignment requirement on the "in" pointer.
        The out pointer should point to length * sizeof(uint32_t) bytes.
        """
        data_ptr = ffi.cast("uint8_t *", ffi.from_buffer(data))
        output = np.empty(n, dtype=np.uint32)
        output_ptr = ffi.cast("uint32_t *", ffi.from_buffer(output))

        if prev is None:
            c_func(data_ptr, output_ptr, n)
        else:
            c_func(data_ptr, output_ptr, n, prev)

        # delta zigzag decode signed type
        if dtype and dtype == np.int16 or dtype == np.int32:
            zigzag = np.empty(n, dtype=np.int32)
            lib.zigzag_delta_decode(
                output_ptr,
                ffi.cast("int32_t *", ffi.from_buffer(zigzag)),
                n, 0
            )
            output = zigzag

        if dtype and output.dtype != dtype:
            return output.astype(dtype)

        return output

    return decode


encode = encode_factory(lib.streamvbyte_encode)
encode_0124 = encode_factory(lib.streamvbyte_encode_0124)
encode_delta = encode_factory(lib.streamvbyte_delta_encode, prev=0)
decode = decode_factory(lib.streamvbyte_decode)
decode_0124 = decode_factory(lib.streamvbyte_decode_0124)
decode_delta = decode_factory(lib.streamvbyte_delta_decode, prev=0)

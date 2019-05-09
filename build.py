"""
Builds the C Python wrapper for libstreamvbyte
"""

from cffi import FFI
from pathlib import Path


src_path = Path("src").resolve()
lib_path = src_path.joinpath("libstreamvbyte.so.0.0.1")
include_path = src_path.joinpath("include")

ffibuilder = FFI()


ffibuilder.set_source(
    "_streamvbyte",
    """
    #include <streamvbyte.h>
    #include <streamvbytedelta.h>
    #include <streamvbyte_zigzag.h>
    """,
    extra_objects=[str(lib_path)],
    include_dirs=[str(include_path)],
    libraries=["c"],
)

ffibuilder.cdef("""
size_t streamvbyte_encode(const uint32_t *in, uint32_t length, uint8_t *out);
size_t streamvbyte_decode(const uint8_t *in, uint32_t *out, uint32_t length);
size_t streamvbyte_encode_0124(const uint32_t *in, uint32_t length, uint8_t *out);
size_t streamvbyte_decode_0124(const uint8_t *in, uint32_t *out, uint32_t length);
size_t streamvbyte_delta_encode(const uint32_t *in, uint32_t length, uint8_t *out, uint32_t prev);
size_t streamvbyte_delta_decode(const uint8_t *in, uint32_t *out, uint32_t length, uint32_t prev);
void zigzag_encode(const int32_t * in, uint32_t * out, size_t N);
void zigzag_delta_encode(const int32_t * in, uint32_t * out, size_t N, int32_t prev);
void zigzag_decode(const uint32_t * in, int32_t * out, size_t N);
void zigzag_delta_decode(const uint32_t * in, int32_t * out, size_t N, int32_t prev);
""")


if __name__ == "__main__":
    ffibuilder.compile()

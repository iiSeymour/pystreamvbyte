# pystreamvbyte

[![Build Status](https://travis-ci.org/iiSeymour/pystreamvbyte.svg?branch=master)](https://travis-ci.org/iiSeymour/pystreamvbyte)

Python bindings to [streamvbyte](https://github.com/lemire/streamvbyte).

## Installing

```
$ pip install --user pystreamvbyte
```

## Example

```python
>>> import numpy as np
>>> from streamvbyte import encode, decode
>>>
>>> size = int(40e6)
>>> dtype = np.uint32  # int16, uint16, int32, uint32 supported
>>> data = np.random.randint(0, 512, size=size, dtype=np.uint32)
>>> data.nbytes
160000000
>>> compressed = encode(data)
>>> compressed.nbytes
70001679
>>> recovered = decode(compressed, size, dtype=dtype)
>>> compressed.nbytes / data.nbytes * 100
43.751049375
```

## Development Quick Start

```
$ git clone --recurse-submodules https://github.com/iiSeymour/pystreamvbyte.git
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make test
```

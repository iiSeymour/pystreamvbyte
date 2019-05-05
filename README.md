# pystreamvbyte

[](https://api.travis-ci.org/iiSeymour/pystreamvbyte.svg?branch=master)

Python bindings to [streamvbyte](https://github.com/lemire/streamvbyte).

## Quick Start

```
$ git clone --recurse-submodules https://github.com/iiSeymour/pystreamvbyte.git
$ python3 setup.py develop
$ make test
```

## Example

```python
import numpy as np
from streamvbyte import encode, decode

size = 40e6
dtype = np.uint32  # int16, uint16, int32, uint32 supported
data = np.random.randint(0, 1e5, size=size, dtype=np.uint32)
compressed = encode(data)
recovered = decode(compress, size, dtype=dtype)
```
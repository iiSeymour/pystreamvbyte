from setuptools import setup
from streamvbyte import __version__

setup(
    name='pystreamvbyte',
    version=__version__,
    install_requires=['numpy', 'numba'],
)

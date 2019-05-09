from setuptools import setup, find_packages

setup(
    name='pystreamvbyte',
    version='0.4.1',
    packages=find_packages(),
    install_requires=['numpy', 'cffi'],
    setup_requires=['cffi', 'wheel'],
    cffi_modules=['streamvbyte/build.py:ffibuilder'],
)

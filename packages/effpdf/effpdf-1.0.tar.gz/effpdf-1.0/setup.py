import setuptools
from setuptools import setup
from pathlib import Path

setuptools.setup(
    name="effpdf",
    version=1.0,
    long_decription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])

)

import setuptools
from pathlib import Path

setuptools.setup(
    name="jakepdf",
    version=0.2,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)

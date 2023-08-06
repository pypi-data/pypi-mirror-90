import pathlib
import setuptools
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "ntk/README.md").read_text()

# This call to setup() does all the work
setup(
    name="ntk",
    version="1.1.0",
    description="Build higher application with combination of base tk,ttk",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/njNafir/ntk",
    author="Nj Nafir",
    author_email="njnafir@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files=[('ntk', ['ntk/icon.ico'])],
    install_requires=[],
    entry_points={},
)
"""
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="attribdict",
    version="0.0.4",
    author="Yiqun Chen",
    author_email="yiqunchen1999@gmail.com",
    description="An easy to use and easy to read dict",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yiqunchen1999/attribdict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
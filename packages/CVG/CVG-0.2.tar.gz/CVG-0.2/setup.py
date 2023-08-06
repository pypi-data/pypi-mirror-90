#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="CVG",
    version="0.2",
    author="Jay9z",
    author_email='jay.cn@outlook.com',
    description=("pure python algorithms of computer vision for computer graphics"),
    url="https://github.com/jay9z/CVG",
    packages=find_packages(),
    install_requires=[
        "numpy==1.19.2",
        "opencv-python==4.4.0.42",
        "Matplotlib",
        "SciPy",
        "PyYAML",
        "Pillow"
    ],
)

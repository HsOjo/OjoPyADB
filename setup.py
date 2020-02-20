#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OjoPyADB",
    version="0.2.0",
    author="HsOjo",
    author_email="hsojo@qq.com",
    keywords='hsojo python3 android adb pyadb ojopyadb',
    description='''HsOjo's Python3 Android Debug Bridge. Support App/File/Input/Display Operation...''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HsOjo/OjoPyADB/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

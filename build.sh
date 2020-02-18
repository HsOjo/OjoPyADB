#!/bin/bash
python setup.py sdist bdist_wheel
rm -fr build *.egg-info
pip install dist/*.whl --upgrade
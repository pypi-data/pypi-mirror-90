#!/bin/bash

## This script will build macosx_10_9 x86_64 wheels; it should be
## executed from the root project directory.

set -e -x

pys=(
    /Library/Frameworks/Python.framework/Versions/3.6/bin/python3
    /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
    /Library/Frameworks/Python.framework/Versions/3.8/bin/python3
)

for py in "${pys[@]}"; do
    $py -m pip install pip setuptools wheel numpy pybind11 -U
    $py -m pip wheel --no-deps . -vv
done

whls=(histmp*.whl)

/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 -m pip install twine delocate

for whl in "${whls[@]}"; do
    /Library/Frameworks/Python.framework/Versions/3.7/bin/delocate-wheel $whl
done

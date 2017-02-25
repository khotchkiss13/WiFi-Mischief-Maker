#!/bin/bash
mkdir pypackages
export PYTHONPATH=$PYTHONPATH:~/pypackages
pip install --target=./pypackages dispy

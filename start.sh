#!/bin/bash

if [ ! -d "./venv/" ]; then
    python3 -m venv venv
    pip install --requirement requirements.txt
fi

python3 ./main.py

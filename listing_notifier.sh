#!/bin/bash
pip install -r requirements.txt

FILE = .env
if [ ! -f "$FILE" ]; then
    echo "$FILE does not exist."
    source ./email_setup.sh
fi

python main.py
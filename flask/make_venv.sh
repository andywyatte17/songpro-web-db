#!/usr/bin/env bash
[ -d "/path/to/dir" ] || python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
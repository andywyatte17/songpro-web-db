#!/usr/bin/env python3
'''
Usage:
  python de-rtf-json.py src.json dst.json
'''
import sys
import json
from striprtf.striprtf import rtf_to_text

with open(sys.argv[1], "r") as f:
    js = json.load(f)

for i in range(len(js)):
    j = js[i]
    for k in j.keys():
        original = j[k]
        if not original.startswith("{\\rtf1"):
            continue
        rtf = rtf_to_text(original)
        rtf = rtf.lstrip("\n").rstrip("\n")
        if original!="" and rtf=="":
            j[k] = ""
        elif original!=rtf:
            j[k] = rtf
    js[i] = j

with open(sys.argv[2], "w") as f:
    json.dump(js, f, indent=2)

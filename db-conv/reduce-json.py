#!/usr/bin/env python3
'''
Usage:
  python3 reduce-json.py input.json output.json count
'''

import sys
import json
import random

with open(sys.argv[1], "r") as f:
    js = json.load(f)

js2 = []
for c in range(int(sys.argv[3])):
    n = random.randint(0, len(js)-1-c)
    js = js[:n] + js[n+1:] + js[n:n+1]
    js2 = js2 + [js[-1]]

with open(sys.argv[2], "w") as f:
    json.dump(js2, f)

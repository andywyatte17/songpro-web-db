import csv
import json
import sys, os
import io
import subprocess

def read_CSV(csvfile):
    csv_rows = []
    reader = csv.DictReader(csvfile)
    field = reader.fieldnames
    for row in reader:
        stuff = {field[i]:row[field[i]] for i in range(len(field))}
        csv_rows.append(stuff)
    return csv_rows

def convert_write_json(data, json_file):
    f = json_file
    f.write(json.dumps(data, sort_keys=False, \
            indent=2, separators=(',', ': ')).encode('utf-8'))

fiS = None
for encoding in ('utf-8', 'cp1252'):
    try:
        with open(sys.argv[1], "rb") as fi0:
            fiS = fi0.read().decode(encoding)
    except:
        continue
    break

fi = io.StringIO(fiS)
csv_rows = read_CSV(fi)

with open(sys.argv[2], "wb") as fo:
    convert_write_json(csv_rows, fo)

import csv
import json
import sys
import io

'''
'''

#Read CSV File
def read_CSV(csvfile, json_file):
    csv_rows = []
    reader = csv.DictReader(csvfile)
    field = reader.fieldnames
    for row in reader:
        csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
    convert_write_json(csv_rows, json_file)

#Convert csv data into json
def convert_write_json(data, json_file):
    f = json_file
    f.write(json.dumps(data, sort_keys=False, \
            indent=2, separators=(',', ': ')).encode('utf-8'))

for encoding in ('utf-8', 'cp1252'):
    try:
        with open(sys.argv[1], "rb") as fi0:
            s = fi0.read().decode(encoding)
    except:
        continue
    break

fi = io.StringIO(s)
with open(sys.argv[2], "wb") as fo:
    read_CSV(fi, fo)


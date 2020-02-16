import json
import sys
import multiprocessing.pool
import multiprocessing
from multiprocessing import Value
import subprocess
import os
import time
import glob

def RtfToMarkdown(s):
    global lock, lookup, counter, total, t0
    s2 = None

    lock.acquire()
    nc = int(time.clock() * 1000000)
    time.sleep(0.001)
    if s in lookup.keys():
        s2 = lookup[s]
        counter.value -= 1
    lock.release()
    if s2: return s2

    NAME = "rtf-pd-{}.rtf".format(nc)
    NAME2 = "rtf-pd-{}.txt".format(nc)
    with open(NAME, "wb") as f:
        f.write(s.encode('utf-8'))
    if os.path.exists(NAME2):
        os.unlink(NAME2)
    
    lock.acquire()
    subprocess.check_output([
        "soffice", 
        "--headless",
        "--convert-to",
        "txt:Text",
        NAME])
    lock.release()

    with open(NAME2, "rb") as f:
        s2 = f.read().decode('utf-8')
    os.unlink(NAME)
    os.unlink(NAME2)

    lock.acquire()
    lookup[s] = s2
    counter.value -= 1
    t1 = time.time() - t0
    done = total - counter.value
    print(counter.value, t1, done, t1/done)
    lock.release()
    return s2

with open(sys.argv[1], "r") as f:
    js = json.load(f)

lock = multiprocessing.Lock()
q = []

for x in js:
    for k in x.keys():
        v = x[k]
        if "rtf" in v:
            q.append( v )

for x in glob.glob("rtf-pd-*.*"):
    os.unlink(x)

total = len(q)
t0 = time.time()
counter = Value('i', len(q))
lookup = {}
pool = multiprocessing.pool.Pool(20)
q2 = pool.map( RtfToMarkdown, q )

#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    node, deg_str = parts
    try:
        deg = int(deg_str)
    except ValueError:
        continue
    print("%d\t1" % deg)

#!/usr/bin/env python
import sys

current_deg = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    deg_str, val_str = parts
    try:
        deg = int(deg_str)
        val = int(val_str)
    except ValueError:
        continue

    if current_deg is None:
        current_deg = deg
        current_count = val
    elif deg == current_deg:
        current_count += val
    else:
        print("%d\t%d" % (current_deg, current_count))
        current_deg = deg
        current_count = val

# flush last degree
if current_deg is not None:
    print("%d\t%d" % (current_deg, current_count))

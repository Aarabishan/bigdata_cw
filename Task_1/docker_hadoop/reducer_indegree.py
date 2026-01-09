#!/usr/bin/env python
import sys

current_node = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    node, val_str = parts
    try:
        val = int(val_str)
    except ValueError:
        continue

    if current_node is None:
        current_node = node
        current_count = val
    elif node == current_node:
        current_count += val
    else:
        print("%s\t%d" % (current_node, current_count))
        current_node = node
        current_count = val

if current_node is not None:
    print("%s\t%d" % (current_node, current_count))

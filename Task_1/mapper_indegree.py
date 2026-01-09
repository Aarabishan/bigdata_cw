#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split()
    if len(parts) < 2:
        continue
    src, dst = parts[0], parts[1]
    print("%s\t1" % dst)



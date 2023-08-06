#!/usr/bin/env python

import os
import sys
import perf

help = """
perf help section

TODO
"""


while True:
    url = input("URL:")
    count = int(input("Count:"))
    location = input("Location (optional):")
    _perf = perf.Perf(url, count=count, location=location)
    gets = _perf.get()
    if _perf.location:
        print(_perf.location)
    print("#\t(s)")
    for k,v in gets.items():
        print(f"{k}\t{v}")



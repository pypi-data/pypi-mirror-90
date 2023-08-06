"""
--- Day 13: Packet Scanners ---
https://adventofcode.com/2017/day/13
"""
from itertools import count

from aocd import data
from parse import parse


def parsed(data):
    d = {}
    for line in data.splitlines():
        result = parse("{depth:d}: {range:d}", line)
        d[result.named["depth"]] = 2 * result.named["range"] - 2
    return d


def severity(d, delay=0):
    return sum(t * (r + 2) // 2 for t, r in d.items() if (t + delay) % r == 0)


def delay(d):
    for t0 in count():
        s = severity(d, delay=t0)
        if not s and t0 % d[0]:
            return t0


d = parsed(data)
print(severity(d))
print(delay(d))

"""Демо-модуль для показа процесса ревью (до исправлений)."""


def f1(items, d=1):
    total = 0
    for it in items:
        total += it["price"] * it["qty"]
    return total / d


def calc2(o):
    s = 0
    for i in o.items:
        s += i["price"] * i["qty"]
    return s


class M:
    def __init__(self, x):
        self.x = x

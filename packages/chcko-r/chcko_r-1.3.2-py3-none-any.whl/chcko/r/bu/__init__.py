# -*- coding: utf-8 -*-
from random import sample
from chcko.chcko.hlp import Struct, norm_int as chorm


def chiven():
    a, c = sample(list(range(2, 9)) + list(range(-9, -2)), 2)
    x = sample(list(range(2, 9)) + list(range(-9, -2)), 1)[0]
    b = (c - a) * x
    g = Struct(a=a, b=b, c=c)
    return g


def chalc(g):
    res = g.b / (g.c - g.a)
    return [res]

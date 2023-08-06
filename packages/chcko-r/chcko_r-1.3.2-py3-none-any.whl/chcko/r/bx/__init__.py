# -*- coding: utf-8 -*-
from random import randrange
from math import pi, sin, cos
from chcko.chcko.hlp import Struct


def chiven():
    c = randrange(4, 20)
    alpha = randrange(10, 80)
    g = Struct(c=c, alpha=alpha)
    return g


def chalc(g):
    res = 0.5 * sin(pi * g.alpha / 180) * cos(pi * g.alpha / 180) * g.c ** 2
    return [res]

# -*- coding: utf-8 -*-

from chcko.chcko.hlp import Struct, norm_frac as chorm
import random
from sympy import Rational as R

__all__ = ['chiven', 'chalc']


def chiven():
    g = Struct()
    g.x = random.sample(list(range(-9, -1)) + list(range(1, 9)), 2)
    g.b = random.sample(list(range(-9, -1)) + list(range(1, 9)), 1)[0]
    return g


def chalc(g):
    res = [R(g.b, g.x[1])]
    return res

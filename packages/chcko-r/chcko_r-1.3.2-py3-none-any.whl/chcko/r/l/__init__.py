# -*- coding: utf-8 -*-

import random
import numpy as np
from chcko.chcko.hlp import Struct, norm_frac as chorm


def chiven():
    r = sorted(random.sample(list(range(-9, -1)) + list(range(1, 9)), 2))
    c = [-1, r[0] + r[1], -r[0] * r[1]]
    g = Struct(r=r, c=c)
    return g


def chalc(g):
    p = np.poly1d(g.c)
    p_i = np.polyint(p)
    I = p_i(g.r[1]) - p_i(g.r[0])
    return [I]

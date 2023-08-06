# -*- coding: utf-8 -*-
from random import sample
from chcko.chcko.hlp import Struct, norm_list, norm_frac

import numpy as np
from numpy.linalg import det


def chiven():
    z = zip("ABC", zip(sample(range(-9, 10), 3), sample(range(-9, 10), 3)))
    g = Struct(z)
    return g


def chalc(g):
    D = (np.array(g.C) + np.array(g.A) - np.array(g.B)).tolist()
    A = int(
        abs(det(np.vstack([np.array(g.C) - np.array(g.B), np.array(g.A) - np.array(g.B)]))))
    return [','.join([str(dd) for dd in D]), str(A)]

chorm = lambda v: norm_list(v, norm_frac)

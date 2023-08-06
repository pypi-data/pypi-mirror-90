# -*- coding: utf-8 -*-

import numpy as np
import random

from chcko.chcko.hlp import Struct


def chiven():
    while True:
        A = np.array(random.sample(list(range(1, 19)) + list(range(-19, -1)), 4))
        A.shape = (2, 2)
        try:
            np.linalg.inv(A)
        except:
            continue
        break
    x = np.array(random.sample(list(range(2, 9)) + list(range(-9, -2)), 2))
    b = np.dot(A, x)
    A = A.tolist()
    b = b.tolist()
    g = Struct(A=A, b=b)
    return g


def chalc(g):
    iA = np.linalg.inv(np.array(g.A))
    x = np.dot(iA, np.array(g.b))
    return [i for i in x.round().tolist()]

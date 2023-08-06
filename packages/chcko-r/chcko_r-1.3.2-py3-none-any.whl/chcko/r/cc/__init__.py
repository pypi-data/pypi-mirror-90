# -*- coding: utf-8 -*-

import numpy as np
import random

from chcko.chcko.hlp import Struct, norm_frac as chorm
import chcko.r.u as ru


def chiven():
    g = ru.chiven()
    g.v = random.sample(range(-9, 9), 2)
    return g

#g.m=np.array([[3./13, 1./13],[4./13, -3./13]])
# g.v=np.array([-6,4])


def chalc(g):
    A = np.linalg.inv(np.array(g.m)).round()
    res = np.dot(A, np.transpose(g.v))
    return res.tolist()

# -*- coding: utf-8 -*-
import random
from sympy.abc import x
from sympy.solvers import solve
from sympy import sstr, apart, S
from chcko.chcko.hlp import Struct, norm_frac as chorm


def chiven():
    a, b, c, d, e, f = random.sample(list(range(-9, -1)) + list(range(1, 9)), 6)
    #x = a/b
    rs = a - c
    ls = b * x - c
    rs = d * rs / ls
    ls = 1 - e * x / (d + e * x)
    rs = rs / (d + e * x)
    rs = apart(rs)
    ls = ls / f
    rs = rs / f
    ls1, ls2 = ls.as_two_terms()
    rs1, rs2 = rs.as_two_terms()
    g = Struct()
    g.sls = sstr(S(ls1) + S(ls2))
    g.srs = sstr(S(rs1) + S(rs2))
    return g


def chalc(g):
    try:
        sol = solve(S(g.sls) - S(g.srs), x)[0]
        return [sol]
    except:
        return ['-']

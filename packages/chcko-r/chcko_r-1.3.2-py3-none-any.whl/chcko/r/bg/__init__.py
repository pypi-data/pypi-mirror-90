# -*- coding: utf-8 -*-
from random import randrange
from chcko.chcko.hlp import Struct, listable


def chiven():
    g = Struct()
    g.b = randrange(20, 128)
    g.a = randrange(3, 12) * g.b
    return g


@listable
def chorm(a):
    return a.lstrip('0')


def chalc(g):
    return ['{0:b}'.format(int(g.a / g.b))]

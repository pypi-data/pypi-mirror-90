# -*- coding: utf-8 -*-
from random import randrange
from chcko.chcko.hlp import Struct, listable


def chiven():
    g = Struct()
    g.a = randrange(20, 128)
    g.b = randrange(20, 128)
    return g


@listable
def chorm(a):
    return a.lstrip('0')


def chalc(g):
    return ['{0:b}'.format(g.a - g.b)]

# -*- coding: utf-8 -*-
from random import randrange
from chcko.chcko.hlp import Struct, listable


def chiven():
    g = Struct()
    g.i = randrange(20, 256)
    return g


@listable
def chorm(a):
    return a.lstrip('0')


def chalc(g):
    return ['{0:b}'.format(g.i)]

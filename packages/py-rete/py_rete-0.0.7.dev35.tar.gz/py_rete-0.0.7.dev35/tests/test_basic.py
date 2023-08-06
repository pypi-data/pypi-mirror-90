# -*- coding: utf-8 -*-
from py_rete.conditions import Cond
from py_rete.conditions import Ncc
from py_rete.common import WME
from py_rete.common import Token
from py_rete.common import V


def test_token():
    tdummy = Token(None, None)
    t0 = Token(tdummy, WME('B1', 'on', 'B2'))

    assert tdummy.parent is None
    assert t0.parent == tdummy

    assert tdummy.children == [t0]
    assert t0.children == []


def test_condition_vars():
    c0 = Cond(V('x'), 'is', V('y'))
    assert len(c0.vars) == 2


def test_condition_contain():
    c0 = Cond(V('a'), V('b'), V('c'))
    assert c0.contain(V('a'))
    assert not c0.contain(V('d'))


def test_condition_test():
    c0 = Cond(V('x'), 'color', 'red')
    w0 = WME('B1', 'color', 'red')
    w1 = WME('B1', 'color', 'blue')
    assert c0.test(w0)
    assert not c0.test(w1)


def test_ncc():
    c0 = Cond(V('a'), V('b'), V('c'))
    c1 = Ncc(Cond(V('x'), 'color', 'red'))
    c2 = Ncc(c0, c1)
    assert c2.number_of_conditions == 2

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os

def get_ofp_testfiles():
    _dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        os.path.sep.join(['test', 'data']))
    return [f for f in os.listdir(_dir)
            if os.path.isfile(os.path.join(_dir, f))
            and os.path.splitext(f)[1] == '.txt']

#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-07-05
#

"""
"""

from __future__ import print_function, unicode_literals

import random
import webbrowser
from time import sleep


PAGES = 20
SLEEP = 40

URL_TEMPLATE = 'http://localhost:5000/all/{colour}'


def random_colour():
    """Generate a random CSS colour"""

    def _rand_hex():
        c = hex(random.randint(0, 254))[2:]
        if len(c) == 1:
            c = '0' + c
        return c

    r = _rand_hex()
    g = _rand_hex()
    b = _rand_hex()
    return '{}{}{}'.format(r, g, b).upper()


for i in range(PAGES):
    url = URL_TEMPLATE.format(colour=random_colour())
    print('Opening preview {} of {}...'.format(i+1, PAGES))
    webbrowser.open(url)
    sleep(SLEEP)

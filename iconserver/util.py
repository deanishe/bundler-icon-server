#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2016 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2016-12-20
#

"""Helper functions."""

from __future__ import print_function, absolute_import

import re


def css_colour(s):
    """Is string a valid CSS colour."""
    m = re.match(r'^(?:[0-9a-fA-Z]{3}){1,2}$', s)
    return m is not None

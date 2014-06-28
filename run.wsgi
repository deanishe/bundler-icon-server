#!env/bin/python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-06-28
#

"""
"""

from __future__ import print_function, unicode_literals

import sys
import os

appdir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if appdir not in sys.path:
    sys.path.insert(0, appdir)

from iconserver import app as application

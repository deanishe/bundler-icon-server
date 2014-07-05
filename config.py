#!/usr/bin/env python
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

import os

from iconserver.font import Font

DEBUG = False

# Default size of icons
SIZE = 128  # px

basedir = os.path.abspath(os.path.dirname(__file__))

# Directory to save generated icons to
CACHEDIR = os.path.join(basedir, 'iconserver', 'static', 'icons')
# URL to CACHEDIR
CACHEURL = None
# Default (for the dev server)
# CACHEURL = 'http://localhost:5000/static/icons'

# Maximum size of the icon cache
# Override this in `siteconfig.py`
MAX_CACHE_SIZE = 0  # Bytes

# Where JSON configuration files are stored
CONFDIR = os.path.join(basedir, 'fonts')

# Where the TTF fonts are saved
FONTDIR = os.path.join(basedir, 'iconserver', 'static', 'fonts')

LOG_PATH = os.path.join(basedir, 'log', 'iconserver.log')
LOG_SIZE = 1024 * 1024  # 1 MB

# Administrators
ADMINS = []

USE_LOCAL_MAIL = True

FONTS = {}

for filename in os.listdir(CONFDIR):
    if not filename.endswith('.json'):
        continue
    path = os.path.join(CONFDIR, filename)
    font = Font.from_json(path)
    FONTS[font['id']] = font


from siteconfig import *

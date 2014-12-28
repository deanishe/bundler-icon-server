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

# Allow API users to specify icon size
API_ALLOW_SIZE = True

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

# HTML Page footer shown at the bottom of each page
# You can include HTML, as this won't be escaped by Jinja

HTML_FOOTER = """
by <a href="http://www.deanishe.net/">Dean Jackson</a>
&nbsp;&nbsp;|&nbsp;
hosted on <a
href="https://www.linode.com/?r=4a30af04867ab319eef6c19a4de9b06620c11dc4"
target="_new">Linode</a>
"""

from siteconfig import *

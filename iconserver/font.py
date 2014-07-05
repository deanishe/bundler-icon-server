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

import sys
import json

if sys.version < '3':
    from codecs import unicode_escape_decode

    def unicodify(x):
        return unicode_escape_decode(x)[0]

else:
    def unicodify(x):
        return x


class Font(dict):

    @classmethod
    def from_json(self, path):
        """Create and return `Font` instance from JSON file at `path`"""
        with open(path, 'rb') as file:
            return Font(json.load(file))

    def unicode_char(self, name):
        """Return a Unicode character for character named `name`"""
        escaped = '\\u{}'.format(self['characters'][name])
        return unicodify(escaped)

    def cssclass(self, name):
        """Return CSS class for character with name `name`"""
        return self['cssclass'].format(name=name)

#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-06-28
#

"""
Generate Python code/CSS for fonts based on TSV config files.
"""

from __future__ import print_function

# from codecs import unicode_escape_decode

# FORMAT = 'python'
FORMAT = 'json'

characters = {}

# filename = 'entypo.tsv'
# filename = 'entypo-social.tsv'
# filename = 'icomoon.tsv'
# filename = 'typicons.tsv'
# filename = 'elusive.tsv'
filename = 'weather.tsv'


with open(filename, 'rb') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        name, code = line.split('\t')
        characters[name.lower()] = code


if FORMAT == 'python':
    for name in sorted(characters):
        print("'{}': '{}',".format(name, characters[name]))


if FORMAT == 'json':
    output = []
    for name in sorted(characters):
        output.append('"{}": "{}",'.format(name, characters[name]))

    print('\n'.join(output).rstrip(','))

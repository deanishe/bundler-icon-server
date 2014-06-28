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
Try to retrieve all icons from the server and see if they work.
"""

from __future__ import print_function, unicode_literals

import sys
import os
import argparse
from urllib2 import urlopen, URLError
from multiprocessing.dummy import Pool

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import FONTS as fonts

MAX_ICONS = False  # for debugging

# HTTP timeout in seconds
TIMEOUT = 10


def check_icon(args):
    """Try to download the icon"""
    font_id, char, url = args
    try:
        response = urlopen(url, timeout=TIMEOUT)
    except URLError as err:
        print('[ERR]\t{}/{} : {}'.format(font_id, char, err), file=sys.stderr)
        return
    status = response.getcode()
    if status != 200:
        print('[ERR/{}]\t{}/{} : {}'.format(status, font_id, char, err))
        return
    print('[OK]\t{}/{}'.format(font_id, char))


def main():
    parser = argparse.ArgumentParser(usage='%(prog)s [options] SERVER_URL',
                                     description=__doc__)
    parser.add_argument(
        '-t', '--threads',
        help='Number of threads (simultaneous connections)',
        dest='threads', default=1, type=int)
    parser.add_argument('server', help='URL of server')
    args = parser.parse_args()

    server = args.server

    if not server.startswith('http://'):
        server = 'http://{}'.format(server)

    icons = []
    for font_id, font in fonts.items():
        for char in font['characters']:
            url = os.path.join(server, 'icon', font_id, '000', char)
            icons.append((font_id, char, url))

    icons.sort()

    print('{} icons to test on {} ...'.format(len(icons), args.server))

    if MAX_ICONS:
        icons = icons[:MAX_ICONS]

    pool = Pool(args.threads)
    pool.map(check_icon, icons)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()

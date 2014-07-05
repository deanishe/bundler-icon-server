#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-07-05
#

"""Delete old icons

Usage: purge_icons.py /path/to/icons/cache

"""

from __future__ import print_function, unicode_literals

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from siteconfig import MAX_CACHE_SIZE

PRUNE_CACHE_TO = 0.5  # How much to cut cache back by

FILETYPE = 'png'
# MAX_ICONS = 100000


def human_size(bytes):
    """Return number of bytes as string with most appropriate unit"""
    if bytes == 0:
        return '0 B'
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'YB']
    bytes = float(bytes)
    i = 0

    while bytes >= 1024 and i < (len(suffixes) - 1):
        bytes /= 1024.0
        i += 1

    if i > 2:
        f = '{:0.2f}'.format(bytes)
    else:
        f = '{:0.1f}'.format(bytes)

    f = f.rstrip('0').rstrip('.')

    return '{} {}'.format(f, suffixes[i])


def delete_empty_directories(dirpath):
    for root, dirnames, filenames in os.walk(dirpath):
        for dirname in dirnames:
            p = os.path.join(root, dirname)
            if not len(os.listdir(p)):
                os.rmdir(p)


def dirsize(dirpath):
    """Get directory size via `du` (`os.stat` doesn't give accurate results)"""
    output = subprocess.check_output(
        ['du', '-k', dirpath]).decode('utf-8').strip()
    return int(output.split('\n')[-1].split()[0].strip()) * 1024


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    dirpath = sys.argv[1]

    print('Max cache size: {}'.format(human_size(MAX_CACHE_SIZE)))

    icons = []
    cache_size = dirsize(dirpath)

    # Walk directory to get filesizes and access times
    for root, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if not filename.endswith('.{}'.format(FILETYPE)):
                continue
            p = os.path.join(root, filename)
            st = os.stat(p)
            # cache_size += st.st_size
            icons.append((st.st_atime, p, st.st_size))

    print('Cache : {} icons, {}'.format(len(icons), human_size(cache_size)))

    # Delete appropriate percentage of icons.
    # Can't use filesizes as Python and `du` give such different results.
    # Relying on Python's filesizes often results in deleting the entire cache.
    # We'll delete the cache to PRUNE_CACHE_TO of MAX_CACHE_SIZE
    if cache_size > MAX_CACHE_SIZE:
        target_size = MAX_CACHE_SIZE * PRUNE_CACHE_TO
        pc = (cache_size - target_size) / float(cache_size)
        count = int(len(icons) * pc)

        print('Cutting cache to {}. Deleting {} icons...'.format(
              human_size(target_size), count))

        icons.sort()  # least-recently accessed first
        deleted = 0
        for atime, path, size in icons:
            os.unlink(path)
            deleted += 1
            if deleted == count:
                break

        delete_empty_directories(dirpath)

        print('{} icons deleted'.format(deleted))

        print('Cache : {}'.format(human_size(dirsize(dirpath))))

if __name__ == '__main__':
    sys.exit(main())

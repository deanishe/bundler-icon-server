#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-07-05
#

"""Delete oldest icons from cache directory."""

from __future__ import print_function, absolute_import

import argparse
import sys
import os
import subprocess

# Add app root to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# How much to cut cache back to
PRUNE_CACHE_TO = 0.5  # 50% of MAX_CACHE_SIZE

FILETYPE = 'png'
# MAX_ICONS = 100000


def log(s, *args):
    """Simple STDERR logger."""
    if args:
        s = s % args
    print(s, file=sys.stderr)


def human_size(bytes):
    """Return number of bytes as string with most appropriate unit."""
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
    """Recursively delete any empty directories under ``dirpath``."""
    for root, dirnames, filenames in os.walk(dirpath, topdown=False):
        for dirname in dirnames:
            p = os.path.join(root, dirname)
            if not len(os.listdir(p)):
                os.rmdir(p)


def dirsize(dirpath):
    """Get directory size via ``du`` (`os.stat` is accurate)."""
    output = subprocess.check_output(
        ['du', '-k', dirpath]).decode('utf-8').strip()
    # first field of last line is size in KiB. Return size in bytes
    return int(output.split('\n')[-1].split()[0].strip()) * 1024


def parse_argv():
    """Parse ARGV with `argparse` and return options."""
    from siteconfig import MAX_CACHE_SIZE

    mb = int(MAX_CACHE_SIZE / 1024.0 / 1024.0)

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('-m', '--max', dest='max',
                   type=int,
                   default=mb,
                   help='maximum size of cache in MB')
    p.add_argument('-n', '--dry-run', dest='dry_run',
                   default=False,
                   action='store_true',
                   help="don't actually delete any files")
    p.add_argument('dir', metavar='<cachedir>')

    o = p.parse_args()
    o.max = o.max * 1024 * 1024
    return o


def main():
    """Run purge script."""
    o = parse_argv()
    log('opts=%r', o)

    log('Max cache size: %s', human_size(o.max))

    icons = []
    cache_size = dirsize(o.dir)

    # Walk directory to get filesizes and access times
    for root, dirnames, filenames in os.walk(o.dir):
        for filename in filenames:
            if not filename.endswith('.{}'.format(FILETYPE)):
                continue
            p = os.path.join(root, filename)
            st = os.stat(p)
            # cache_size += st.st_size
            icons.append((st.st_atime, p, st.st_size))

    log('Cache : %d icon(s), %s', len(icons), human_size(cache_size))

    # Delete appropriate percentage of icons.
    # Can't use filesizes as Python and `du` give such different results.
    # Relying on Python's filesizes often results in deleting the entire cache.
    #
    # Delete the cache to PRUNE_CACHE_TO of specified max size.

    if cache_size > o.max:
        target_size = o.max * PRUNE_CACHE_TO
        pc = (cache_size - target_size) / float(cache_size)
        count = int(len(icons) * pc)

        log('Cutting cache to %s. Deleting %d icon(s) ...',
            human_size(target_size), count)

        icons.sort()  # least-recently accessed first
        deleted = 0
        for atime, path, size in icons:
            if o.dry_run:
                log('Would delete %r', path)
            else:
                os.unlink(path)
            deleted += 1
            if deleted == count:
                break

        delete_empty_directories(o.dir)

        log('%d icons deleted', deleted)

        log('Cache : %s', human_size(dirsize(o.dir)))

if __name__ == '__main__':
    sys.exit(main())

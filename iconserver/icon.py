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

import os
import re
from time import time

from PIL import Image, ImageFont, ImageDraw

from flask import url_for
from iconserver import app

import config


class Icon(object):

    css_colour = re.compile(r'[a-fA-F0-9]+').match

    def __init__(self, font, colour, character, size=None):
        self.font = font
        self.colour = colour
        self.character = config.FONTS[font].unicode_char(character)
        self.size = size or config.SIZE
        self._ttf = os.path.join(config.FONTDIR, config.FONTS[font]['ttf'])
        self._icons = config.FONTS[font]['characters']
        self._cachepath = os.path.join(
            config.CACHEDIR,
            '{}/{}/{}-{}.png'.format(font, colour, character, self.size))

    def save(self):
        """Generate and save the image to the appropriate cache file"""
        start = time()

        image = Image.new("RGBA", (self.size, self.size),
                          color=(0, 0, 0, 0))

        draw = ImageDraw.Draw(image)

        # Initialize font
        font = ImageFont.truetype(self._ttf, self.size)

        colour = self.colour
        # add hash if colour is CSS format
        if self.css_colour(colour) and len(colour) in (3, 6):
            colour = '#' + self.colour

        # Determine the dimensions of the icon
        size = draw.textsize(self.character, font=font)
        offset = font.getoffset(self.character)

        width, height = map(sum, zip(size, offset))

        draw.text(((self.size - width) / 2, (self.size - height) / 2),
                  self.character,
                  font=font, fill=colour)

        # Get bounding box
        bbox = image.getbbox()

        # Create an alpha mask
        imagemask = Image.new("L", (self.size, self.size), 0)
        drawmask = ImageDraw.Draw(imagemask)

        # Draw the icon on the mask
        drawmask.text(((self.size - width) / 2,
                      (self.size - height) / 2), self.character,
                      font=font, fill=255)

        # Create a solid colour image and apply the mask
        iconimage = Image.new("RGBA", (self.size, self.size), colour)
        iconimage.putalpha(imagemask)

        if bbox:
            iconimage = iconimage.crop(bbox)

        borderw = int((self.size - (bbox[2] - bbox[0])) / 2)
        borderh = int((self.size - (bbox[3] - bbox[1])) / 2)

        # Create output image
        outimage = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        outimage.paste(iconimage, (borderw, borderh))

        # Save file
        dirpath = os.path.dirname(self._cachepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath, 0755)

        outimage.save(self._cachepath)

        app.logger.info('Generated `{}` in {:0.4f} s'.format(
                        self._cachepath, time() - start))

    @property
    def path(self):
        if not os.path.exists(self._cachepath):
            self.save()
        return self._cachepath

    @property
    def url(self):

        filename = self.path.replace(config.CACHEDIR, '').lstrip('/')

        if config.CACHEURL is not None:
            baseurl = config.CACHEURL
        else:
            baseurl = url_for('static', filename='icons')

        return os.path.join(baseurl, filename)

        filename = self.path.replace(config.CACHEDIR, 'icons').lstrip('/')
        return url_for('static', filename=filename)

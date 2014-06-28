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
Generate a PNG of the specified character and font.
"""

from __future__ import unicode_literals

import os
import re

from PIL import Image, ImageFont, ImageDraw

from iconserver import app
from flask import render_template, url_for, redirect, Response, abort

import config


class IconError(Exception):
    """Raised if an icon cannot be generated"""


class Icon(object):

    css_colour = re.compile(r'[a-fA-F0-9]+').match

    def __init__(self, font, colour, character, size=None):
        self.font = font
        self.colour = colour
        self.character = character
        self.size = size or config.SIZE
        self._ttf = os.path.join(config.FONTDIR, config.FONTS[font]['ttf'])
        self._icons = config.FONTS[font]['characters']
        self._cachepath = os.path.join(
            config.CACHEDIR,
            '{}/{}/{}.png'.format(font, colour, character))

    def save(self):
        """Generate and save the image to the appropriate cache file"""
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
        width, height = draw.textsize(self._icons[self.character],
                                      font=font)

        draw.text(((self.size - width) / 2, (self.size - height) / 2),
                  self._icons[self.character],
                  font=font, fill=colour)

        # Get bounding box
        bbox = image.getbbox()

        # Create an alpha mask
        imagemask = Image.new("L", (self.size, self.size), 0)
        drawmask = ImageDraw.Draw(imagemask)

        # Draw the icon on the mask
        drawmask.text(((self.size - width) / 2,
                      (self.size - height) / 2), self._icons[self.character],
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


########################################################################
# Error handlers
########################################################################

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500


def error_text(message, status=400):
    return Response(message, status, mimetype='text/plain')


########################################################################
# Error handlers
########################################################################

@app.route('/icon/<font>/<colour>/<character>')
def get_icon(font, colour, character):

    if font not in config.FONTS:
        return error_text('Unknown font: {}'.format(font), 404)

    if character.lower().endswith('.png'):
        character = character[:-4]

    if character not in config.FONTS[font]['characters']:
        return error_text('Unknown character: {}'.format(character), 404)

    try:
        icon = Icon(font, colour, character)
        return redirect(icon.url)
    except ValueError as err:
        if 'color' in err.message:
            return error_text('Invalid colour: {}'.format(colour), 400)
        # Re-raise error
        raise err


@app.route('/preview/<font>')
def preview(font):
    font = config.FONTS.get(font)
    if font is None:
        abort(404)

    return render_template('preview.html', font=font)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

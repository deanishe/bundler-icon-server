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

import re

from iconserver import app
from flask import render_template, redirect, Response, abort

import config
from icon import Icon


css_colour = re.compile(r'[a-f0-9]+').match


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
# Exported views
########################################################################

@app.route('/icon/<font>/<colour>/<character>')
def get_icon(font, colour, character):

    # Normalise arguments to minimise number of cached images
    colour = colour.lower()
    font = font.lower()
    character = character.lower()

    if not css_colour(colour) or not len(colour) in (3, 6):  # Invalid colour
        return error_text('Invalid colour: {}'.format(colour), 400)

    if len(colour) == 3:  # Expand to full 6 characters
        r, g, b = colour
        colour = '{r}{r}{g}{g}{b}{b}'.format(r=r, g=g, b=b)

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


@app.route('/all')
@app.route('/all/<colour>')
def viewall(colour='444'):
    fonts = []
    names = sorted(config.FONTS.keys())
    for name in names:
        l = []
        font = config.FONTS[name]
        for c in sorted(font['characters']):
            l.append((name, c))
        fonts.append(l)
    rows = map(None, *fonts)
    return render_template('viewall.html', rows=rows, colour=colour)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

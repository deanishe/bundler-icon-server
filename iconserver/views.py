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
from flask import render_template, redirect, Response, abort, request

import config
from icon import Icon
import fonts


css_colour = re.compile(r'[a-f0-9]+').match


########################################################################
# Error handlers
########################################################################

@app.errorhandler(404)
@app.errorhandler(500)
def error_page(error):
    # app.logger.debug('{}\n{}'.format(error.__class__, dir(error)))
    if not hasattr(error, 'code'):
        code = 500
    else:
        code = error.code
    if not hasattr(error, 'description'):
        msg = 'Application error. The administrator has been notified.'
    else:
        msg = error.description
    return render_template('error.html', code=code, message=msg), code


def error_text(message, status=400):
    """Return plain text error message. Used for `API` calls"""
    return Response(message, status, mimetype='text/plain')


########################################################################
# Exported views
########################################################################

@app.route('/icon/<font>/<colour>/<character>/<size>')
@app.route('/icon/<font>/<colour>/<character>')
def get_icon(font, colour, character, size=None):
    """Redirect to static icon path, creating it first if necessary

    :param font: ID of the font, e.g. ``fontawesome``
    :param colour: CSS colour without preceding ``#``, e.g. ``000``
        or ``eeeeee``
    :param character: Name of the character, e.g. ``youtube``
    :param size: Size of the icon in pixels
    """

    # Normalise arguments to minimise number of cached images
    colour = colour.lower()
    font = font.lower()
    character = character.lower()

    # Set size to default if size is disabled in API
    if size is None or not config.API_ALLOW_SIZE:
        size = config.SIZE
    else:
        if size.lower().endswith('.png'):
            size = size[:-4]
        try:
            size = int(size)
        except ValueError as err:
            return error_text('invalid size : {}'.format(size), 400)

    if not css_colour(colour) or not len(colour) in (3, 6):  # Invalid colour
        return error_text('Invalid colour: {}'.format(colour), 400)

    if len(colour) == 3:  # Expand to full 6 characters
        r, g, b = colour
        colour = '{r}{r}{g}{g}{b}{b}'.format(r=r, g=g, b=b)

    if font not in fonts.FONTS:
        return error_text('Unknown font: {}'.format(font), 404)

    if character.lower().endswith('.png'):
        character = character[:-4]

    if character not in fonts.FONTS[font]['characters']:
        return error_text('Unknown character: {}'.format(character), 404)

    try:
        icon = Icon(font, colour, character, size)
        return redirect(icon.url)
    except ValueError as err:
        if 'color' in err.message:
            return error_text('Invalid colour: {}'.format(colour), 400)
        # Re-raise error
        raise err


@app.route('/preview/<font>')
def preview(font):
    """Show preview of all icons/characters available in ``font``"""
    font = fonts.FONTS.get(font)
    if font is None:
        abort(404)

    return render_template('preview.html', font=font)


@app.route('/preview/system')
def preview_system():
    """Show preview of system icons"""

    return render_template('preview-system.html')


@app.route('/')
@app.route('/index')
def index():
    """Homepage"""
    return render_template('index.html', fonts=fonts.FONTS)


@app.route('/search')
@app.route('/search/')
def search():
    """Search installed icons"""
    query = request.args.get('query', '')
    results = []
    matched_fonts = set()
    if query:
        for char, id_ in fonts.CHARACTERS:
            if char.lower().startswith(query.lower()):
                results.append((0, char, id_))
                matched_fonts.add(id_)
            elif query.lower() in char.lower():
                results.append((1, char, id_))
                matched_fonts.add(id_)
        results.sort()

    if results:
        results = [(char, fonts.FONTS[id_]) for (_, char, id_) in results]

    return render_template('search.html', query=query, results=results,
                           fonts=fonts, matched_fonts=matched_fonts)


# Debugging views
#-----------------------------------------------------------------------

@app.route('/all')
@app.route('/all/<colour>')
def viewall(colour='444'):
    """Show all characters in all fonts in colour ``colour``.

    Only active if `config.DEBUG` is ``True``

    """

    if not config.DEBUG:
        abort(404)
    font_list = []
    names = sorted(fonts.FONTS.keys())
    for name in names:
        l = []
        font = fonts.FONTS[name]
        for c in sorted(font['characters']):
            l.append((name, c))
        font_list.append(l)
    rows = map(None, *font_list)
    return render_template('viewall.html', rows=rows, colour=colour)


@app.route('/error/<int:errnum>')
def throwerror(errnum):
    """Throw the specified error to test server error handling"""

    if not config.DEBUG:
        abort(404)

    abort(errnum)

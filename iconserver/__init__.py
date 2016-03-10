#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-07-06
#

"""
"""

from flask import Flask

import config

app = Flask(__name__)
app.config.from_object('config')

if config.MAX_CACHE_SIZE == 0:
    raise ValueError('Set MAX_CACHE_SIZE in siteconfig.py')

from iconserver import views

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler, SMTPHandler

    if config.USE_LOCAL_MAIL:
        import subprocess

        class MailHandler(logging.Handler):

            def emit(self, record):
                msg = self.format(record)
                cmd = ['mail', '-a',
                       'From:no-reply@deanishe.net',
                       '-s', 'Iconserver Error',
                       ', '.join(config.ADMINS)]
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                p.stdin.write(msg)
                p.stdin.close()
                retcode = p.wait()
                if retcode:
                    print('mail returned : {}'.format(retcode))
        mail_handler = MailHandler()

    else:
        from config import MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
        credentials = None
        if MAIL_USERNAME and MAIL_PASSWORD:
            credentials = (MAIL_USERNAME, MAIL_PASSWORD)
        mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                                   'no-reply@deanishe.net',
                                   config.ADMINS,
                                   'Iconserver Error',
                                   credentials,
                                   (None, None))

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    file_handler = RotatingFileHandler(config.LOG_PATH, 'a',
                                       config.LOG_SIZE, 10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

app.logger.info('Iconserver startup')

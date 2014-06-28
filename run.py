#!env/bin/python

from iconserver import app
from iconserver import config

app.run(debug=config.DEBUG)

#!/bin/bash

here=$(dirname "$0")
curdir=$(pwd)
cd "$here"

# Create virtualenv and install server dependencies into it
[[ ! -d "env" ]] && {
	echo "Creating virtualenv ..."
	virtualenv env
}
echo "Installing required packages ..."
env/bin/pip install -r requirements.txt

# Create directories needed for the server to run
echo "Creating directories ..."

[[ ! -d "log" ]] && mkdir log
[[ ! -d "iconserver/static/icons" ]] && mkdir "iconserver/static/icons"

# Create sample configuration file
[[ ! -f siteconfig.py ]] && {
	echo "Creating siteconfig.py"
	cp siteconfig.sample.py siteconfig.py
}

cd -

echo 'Run `run.py` to start the test server at localhost:5000'
echo 'Be sure to edit `siteconfig.py` first, otherwise the server will not run!'

#!/bin/zsh

here=$(dirname "$0")
curdir=$(pwd)
chdir "$here"
[[ ! -d "env" ]] && {
	echo "Creating virtualenv ..."
	virtualenv env
}
echo "Installing required packages ..."
env/bin/pip install -r requirements.txt
chdir "$curdir"

echo "Run `run.py` to start the test server at localhost:5000"

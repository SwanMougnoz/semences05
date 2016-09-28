SHELL=/bin/bash

all:

clean:
	rm -rf ./var

env:
	virtualenv -p python venv
	venv/bin/pip install --upgrade pip setuptools
	venv/bin/pip install --upgrade -r requirements.txt
	venv/bin/pip install -e .
	mkdir -p var

server:
	./dev runserver 0.0.0.0:8000

db:
	./dev makemigrations
	./dev makemigrations semences05
	./dev migrate

tests:
	./dev test -p '*_test.py'

cleanenv: clean env


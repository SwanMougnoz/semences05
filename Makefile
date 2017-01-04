SHELL=/bin/bash

ifeq ($(PROD),true)
    SCRIPT = DJANGO_SETTINGS_MODULE=semences05.settings.prod python manage.py
    PIP = pip
else
    SCRIPT = ./dev
    PIP = venv/bin/pip
endif

clean:
	rm -rf ./var

env:
    ifneq ($(PROD),true)
		virtualenv -p python venv
    endif
	$(PIP) install --upgrade pip setuptools
	$(PIP) install --upgrade -r requirements.txt
	$(PIP) install -e .
	mkdir -p var

server:
	$(SCRIPT) runserver 0.0.0.0:8000

db:
	$(SCRIPT) makemigrations
	$(SCRIPT) makemigrations s5vitrine
	$(SCRIPT) makemigrations s5appadherant
	$(SCRIPT) migrate

db_initial:
	$(script) loaddata initial_data.yaml

tests:
	$(SCRIPT) test

bower:
	$(SCRIPT) bower install

clean_bytescode:
	find -name "*.pyc" -not -path "./venv/*" | xargs rm

static:
	$(SCRIPT) collectstatic

cleanenv: clean env


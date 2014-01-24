# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
ROOT_DIR = $(shell pwd)
DATA_DIR = $(ROOT_DIR)/var
VIRTUALENV_DIR = $(ROOT_DIR)/lib/virtualenv
BIN_DIR = $(VIRTUALENV_DIR)/bin
PIP = $(BIN_DIR)/pip
WGET = wget
PYTHON = $(BIN_DIR)/python
PROJECT = $(shell $(PYTHON) -c "import setup; print setup.NAME")
PACKAGE = $(shell $(PYTHON) -c "import setup; print setup.PACKAGES[0]")
NOSE = $(BIN_DIR)/nosetests


configure:
	# Configuration is stored in etc/ folder. Not generated yet.


develop: directories pip


virtualenv:
	if [ ! -d $(VIRTUALENV_DIR)/bin/ ]; then virtualenv --no-site-packages $(VIRTUALENV_DIR); fi
	$(PIP) install -r $(ROOT_DIR)/etc/virtualenv.cfg


pip: virtualenv
	$(PIP) install -r etc/ci-requirements.txt


directories:
	mkdir -p var/docs
	mkdir -p docs/_static
	mkdir -p var/test


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete
	find $(ROOT_DIR)/ -name ".noseids" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info
	rm -rf $(ROOT_DIR)/demo/*.egg-info


maintainer-clean: distclean
	rm -rf $(BIN_DIR)/
	rm -rf $(ROOT_DIR)/lib/


test: test-app test-demo test-documentation


test-app:
	$(BIN_DIR)/demo test --nose-verbosity=2 -c $(ROOT_DIR)/etc/nose/base.cfg -c $(ROOT_DIR)/etc/nose/$(PACKAGE).cfg django_downloadview
	mv $(ROOT_DIR)/.coverage $(ROOT_DIR)/var/test/app.coverage


test-demo:
	$(BIN_DIR)/demo test --nose-verbosity=2
	mv $(ROOT_DIR)/.coverage $(ROOT_DIR)/var/test/demo.coverage


test-documentation:
	$(NOSE) -c $(ROOT_DIR)/etc/nose/base.cfg sphinxcontrib.testbuild.tests


sphinx:
	make --directory=docs clean html doctest


documentation: sphinx


demo: develop
	$(BIN_DIR)/demo syncdb --noinput
	# Install fixtures.
	mkdir -p var/media
	cp -r $(ROOT_DIR)/demo/demoproject/fixtures var/media/object
	cp -r $(ROOT_DIR)/demo/demoproject/fixtures var/media/object-other
	cp -r $(ROOT_DIR)/demo/demoproject/fixtures var/media/nginx
	$(BIN_DIR)/demo loaddata demo.json


runserver: demo
	$(BIN_DIR)/demo runserver


release:
	$(BIN_DIR)/fullrelease

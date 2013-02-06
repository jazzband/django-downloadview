# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
PROJECT = 'django-downloadview'
ROOT_DIR = $(shell pwd)
DATA_DIR = $(ROOT_DIR)/var
WGET = wget
PYTHON = python
BUILDOUT_CFG = $(ROOT_DIR)/etc/buildout.cfg
BUILDOUT_BOOTSTRAP_URL = https://raw.github.com/buildout/buildout/1.7.0/bootstrap/bootstrap.py
BUILDOUT_BOOTSTRAP = $(ROOT_DIR)/lib/buildout/bootstrap.py
BUILDOUT_BOOTSTRAP_ARGS = -c $(BUILDOUT_CFG) --distribute buildout:directory=$(ROOT_DIR)
BUILDOUT = $(ROOT_DIR)/bin/buildout
BUILDOUT_ARGS = -N -c $(BUILDOUT_CFG) buildout:directory=$(ROOT_DIR)


configure:
	# Configuration is stored in etc/ folder.


develop: buildout


buildout:
	# Download zc.buildout bootstrap.
	if [ ! -f $(BUILDOUT_BOOTSTRAP) ]; then \
	    mkdir -p $(ROOT_DIR)/lib/buildout; \
	    $(WGET) $(BUILDOUT_BOOTSTRAP_URL) -O $(BUILDOUT_BOOTSTRAP); \
	fi
	# Bootstrap buildout.
	if [ ! -f $(BUILDOUT) ]; then \
	    $(PYTHON) $(BUILDOUT_BOOTSTRAP) $(BUILDOUT_BOOTSTRAP_ARGS); \
	fi
	# Run zc.buildout.
	$(BUILDOUT) $(BUILDOUT_ARGS)


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete
	find $(ROOT_DIR)/ -name ".noseids" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info
	rm -rf $(ROOT_DIR)/demo/*.egg-info


maintainer-clean: distclean
	rm -rf $(ROOT_DIR)/bin/
	rm -rf $(ROOT_DIR)/lib/


test: test-demo test-documentation


test-demo:
	bin/demo test demo
	mv $(ROOT_DIR)/.coverage $(ROOT_DIR)/var/test/demo.coverage


test-documentation:
	bin/nosetests -c $(ROOT_DIR)/etc/nose.cfg sphinxcontrib.testbuild.tests


apidoc:
	cp docs/api/index.txt docs/api-backup.txt
	rm -rf docs/api/*
	mv docs/api-backup.txt docs/api/index.txt
	bin/sphinx-apidoc --suffix txt --output-dir $(ROOT_DIR)/docs/api django_downloadview


sphinx:
	make --directory=docs clean html doctest


documentation: apidoc sphinx


demo: develop
	mkdir -p var/media/document
	bin/demo syncdb --noinput
	cp $(ROOT_DIR)/demo/demoproject/download/fixtures/hello-world.txt var/media/document/
	bin/demo loaddata $(ROOT_DIR)/demo/demoproject/download/fixtures/demo.json
	bin/demo runserver


release:
	bin/fullrelease

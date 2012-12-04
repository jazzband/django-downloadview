# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
PROJECT = 'django-downloadview'
ROOT_DIR = $(shell pwd)
DATA_DIR = $(ROOT_DIR)/var
WGET = wget
PYTHON = python
BUILDOUT_BOOTSTRAP_URL = https://raw.github.com/buildout/buildout/1.6.3/bootstrap/bootstrap.py
BUILDOUT_BOOTSTRAP = $(ROOT_DIR)/lib/buildout/bootstrap.py
BUILDOUT = $(ROOT_DIR)/bin/buildout
BUILDOUT_ARGS = -N


buildout:
	# Download zc.buildout bootstrap.
	if [ ! -f $(BUILDOUT_BOOTSTRAP) ]; then \
	    mkdir -p $(ROOT_DIR)/lib/buildout; \
	    $(WGET) $(BUILDOUT_BOOTSTRAP_URL) -O $(BUILDOUT_BOOTSTRAP); \
	fi
	# Bootstrap buildout.
	if [ ! -f $(BUILDOUT) ]; then \
	    $(PYTHON) $(BUILDOUT_BOOTSTRAP) --distribute; \
	fi
	# Run zc.buildout.
	$(BUILDOUT) $(BUILDOUT_ARGS)


develop: buildout


update: develop


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete
	find $(ROOT_DIR)/ -name ".noseids" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info
	rm -rf $(ROOT_DIR)/demo/*.egg-info


maintainer-clean: distclean
	rm -rf $(ROOT_DIR)/bin/
	rm -rf $(ROOT_DIR)/lib/


test:
	bin/demo test demo


apidoc:
	cp docs/api/index.txt docs/api-backup.txt
	rm -rf docs/api/*
	mv docs/api-backup.txt docs/api/index.txt
	bin/sphinx-apidoc --suffix txt --output-dir $(ROOT_DIR)/docs/api django_downloadview


sphinx:
	make --directory=docs clean html doctest


documentation: apidoc sphinx


runserver:
	bin/demo runserver


demo: develop runserver


release:
	bin/fullrelease

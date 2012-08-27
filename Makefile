# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
PROJECT = 'django-downloadview'
ROOT_DIR = $(shell pwd)
DATA_DIR = $(ROOT_DIR)/var
VIRTUALENV = virtualenv
VIRTUALENV_DIR = $(ROOT_DIR)/lib/virtualenv
PIP = $(VIRTUALENV_DIR)/bin/pip
BUILDOUT = $(ROOT_DIR)/bin/buildout
BUILDOUT_ARGS = -N


virtualenv:
	if [ ! -x $(PIP) ]; then \
	    if [[ "`$(VIRTUALENV) --version`" < "`echo '1.8'`" ]]; then \
	        $(VIRTUALENV) --no-site-packages --distribute $(VIRTUALENV_DIR); \
	    else \
	        $(VIRTUALENV) $(VIRTUALENV_DIR); \
	    fi; \
	    $(PIP) install -U pip; \
	fi


buildout:
	# Install zc.buildout.
	if [ ! -x $(BUILDOUT) ]; then \
	    mkdir -p $(ROOT_DIR)/lib/buildout; \
	    $(PIP) install zc.buildout; \
	    mkdir -p `dirname $(BUILDOUT)`; \
	    ln -s $(VIRTUALENV_DIR)/bin/buildout $(BUILDOUT); \
	fi
	# Run zc.buildout.
	$(BUILDOUT) $(BUILDOUT_ARGS)


develop: virtualenv buildout


update: develop


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info


maintainer-clean: distclean
	rm -rf $(ROOT_DIR)/bin/
	rm -rf $(ROOT_DIR)/lib/


test:
	#bin/nosetests --config=etc/nose.cfg
	bin/demo test download


documentation:
	make --directory=docs clean html doctest


release:
	bin/fullrelease

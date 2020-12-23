# Reference card for usual actions in development environment.
#
# For standard installation of django-downloadview as a library, see INSTALL.
#
# For details about django-downloadview's development environment, see
# CONTRIBUTING.rst.
#
PIP = pip
TOX = tox
BLACK = black
ISORT = isort

#: help - Display callable targets.
.PHONY: help
help:
	@echo "Reference card for usual actions in development environment."
	@echo "Here are available targets:"
	@egrep -o "^#: (.+)" [Mm]akefile  | sed 's/#: /* /'


#: develop - Install minimal development utilities.
.PHONY: develop
develop:
	$(PIP) install -e .


#: clean - Basic cleanup, mostly temporary files.
.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name '*.pyo' -delete
	find . -name "__pycache__" -delete


#: distclean - Remove local builds, such as *.egg-info.
.PHONY: distclean
distclean: clean
	rm -rf *.egg
	rm -rf *.egg-info
	rm -rf demo/*.egg-info


#: maintainer-clean - Remove almost everything that can be re-generated.
.PHONY: maintainer-clean
maintainer-clean: distclean
	rm -rf build/
	rm -rf dist/
	rm -rf .tox/


#: test - Run test suites.
.PHONY: test
test:
	mkdir -p var
	$(PIP) install -e .[test]
	$(TOX)


#: documentation - Build documentation (Sphinx, README, ...)
.PHONY: documentation
documentation: sphinx readme


#: sphinx - Build Sphinx documentation (docs).
.PHONY: sphinx
sphinx:
	$(TOX) -e sphinx


#: readme - Build standalone documentation files (README, CONTRIBUTING...).
.PHONY: readme
readme:
	$(TOX) -e readme


#: demo - Setup demo project.
.PHONY: demo
demo:
	pip install -e .
	pip install -e demo
	demo migrate --noinput
	# Install fixtures.
	mkdir -p var/media/object var/media/object-other/ var/media/nginx
	cp -r demo/demoproject/fixtures/* var/media/object/
	cp -r demo/demoproject/fixtures/* var/media/object-other/
	cp -r demo/demoproject/fixtures/* var/media/nginx/
	demo loaddata demo.json


#: runserver - Run demo server.
.PHONY: runserver
runserver: demo
	demo runserver

.PHONY: black
black:
	$(BLACK) demo tests django_downloadview

.PHONY: isort
isort:
	$(ISORT) --recursive django_downloadview tests demo

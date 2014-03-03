# Reference card for usual actions in development environment.
#
# For standard installation of django-downloadview as a library, see INSTALL.
#
# For details about django-downloadview's development environment, see
# CONTRIBUTING.rst.
#
PIP = pip
TOX = tox


.PHONY: all help develop clean distclean maintainer-clean test documentation sphinx readme demo runserver release


# Default target. Does nothing.
all:
	@echo "Reference card for usual actions in development environment."
	@echo "Nothing to do by default."
	@echo "Try 'make help'."


#: help - Display callable targets.
help:
	@echo "Reference card for usual actions in development environment."
	@echo "Here are available targets:"
	@egrep -o "^#: (.+)" [Mm]akefile  | sed 's/#: /* /'


#: develop - Install minimal development utilities such as tox.
develop:
	$(PIP) install tox
	$(PIP) install -e ./
	$(PIP) install -e ./demo/


#: clean - Basic cleanup, mostly temporary files.
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name ".noseids" -delete


#: distclean - Remove local builds, such as *.egg-info.
distclean: clean
	rm -rf *.egg
	rm -rf *.egg-info
	rm -rf demo/*.egg-info


#: maintainer-clean - Remove almost everything that can be re-generated.
maintainer-clean: distclean
	rm -rf bin/
	rm -rf lib/
	rm -rf build/
	rm -rf dist/
	rm -rf .tox/


#: test - Run full test suite.
test:
	$(TOX)


#: sphinx - Build Sphinx documentation.
sphinx:
	$(TOX) -e sphinx


#: readme - Build standalone documentation files (README, CONTRIBUTING...).
readme:
	$(TOX) -e readme


#: documentation - Build full documentation.
documentation: sphinx readme


demo: develop
	demo syncdb --noinput
	# Install fixtures.
	mkdir -p var/media
	cp -r demo/demoproject/fixtures var/media/object
	cp -r demo/demoproject/fixtures var/media/object-other
	cp -r demo/demoproject/fixtures var/media/nginx
	demo loaddata demo.json


runserver: demo
	demo runserver


#: release - Tag and push to PyPI.
release:
	$(TOX) -e release

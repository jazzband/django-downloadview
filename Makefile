# Reference card for usual actions in development environment.
#
# For standard installation of hospital as a library, see INSTALL.
# For details about hospital's development environment, see CONTRIBUTING.rst.


develop:
	pip install tox zest.releaser
	pip install -e ./
	pip install -e ./demo/


clean:
	find . -name "*.pyc" -delete
	find . -name ".noseids" -delete


distclean: clean
	rm -rf *.egg-info
	rm -rf demo/*.egg-info


maintainer-clean: distclean
	rm -rf bin/
	rm -rf lib/
	rm -rf build/
	rm -rf dist/
	rm -rf .tox/


test:
	tox


test-app:
	tox -e py27


test-demo:
	tox -e demo


sphinx:
	tox -e sphinx


documentation: sphinx


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


release:
	fullrelease

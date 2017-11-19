PACKAGE_NAME =    $(shell python setup.py --name)
PACKAGE_VERSION = $(shell python setup.py --version)

dist:
	python setup.py sdist

upload: dist
	twine upload dist/$(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz

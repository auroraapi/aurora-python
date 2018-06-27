PACKAGE_NAME =    $(shell python setup.py --name)
PACKAGE_VERSION = $(shell python setup.py --version)

.PHONY: dist

dist:
	python setup.py sdist

upload: dist
	twine upload dist/$(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz

test:
	python3 setup.py test

clean:
	find . -name "*.pyc" -exec rm -rf {} \+
	find . -name "__pycache__" -exec rm -rf {} \+
	rm -rf .pytest_cache htmlcov .coverage

clean-all: clean
	rm -rf .eggs *.egg-info dist


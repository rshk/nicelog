## Standard makefile for Python tests

BASE_PACKAGE = nicelog

.PHONY: all upload package install install_dev test docs publish_docs

all: help

help:
	@echo "AVAILABLE TARGETS"
	@echo "----------------------------------------"
	@echo "pypi_upload - build source distribution and upload to pypi"
	@echo "pypi_register - register proejct on pypi"
	@echo "package - build sdist and py2/py3 wheels"
	@echo "twine_upload - upload via twine"
	@echo
	@echo "install - install project in production mode"
	@echo "install_dev - install project in development mode"
	@echo
	@echo "test - run tests"
	@echo "setup_tests - install dependencies for tests"
	@echo
	@echo "docs - build documentation (HTML)"
	@echo "publish_docs - publish documentation to GitHub pages"

pypi_register:
	python setup.py register -r https://pypi.python.org/pypi

pypi_upload:
	python setup.py sdist upload -r https://pypi.python.org/pypi

package:
	python3 setup.py sdist bdist_wheel
	python2 setup.py bdist_wheel

clean_package:
	rm -f dist/*

twine_upload:
	twine upload dist/*

install:
	python setup.py install

install_dev:
	python setup.py develop

test:
	py.test -vvv --pep8 --cov=$(BASE_PACKAGE) --cov-report=term-missing ./tests

manual_test:
	PYTHONPATH=scripts python -m manual_test

setup_tests:
	pip install -U -r ./tests/requirements.txt

docs:
	$(MAKE) -C docs html

publish_docs: docs
	ghp-import -n -p ./docs/build/html
	@echo
	@echo "HTML output published on github-pages"

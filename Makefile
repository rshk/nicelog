.PHONY: all upload

all:
	@echo "You must specify a target"
	@echo "upload - build source distribution and upload to pypi"

upload:
	python setup.py sdist upload -r https://pypi.python.org/pypi

#!/bin/bash
python setup.py sdist bdist_wheel
twine check dist/*
# For testing
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
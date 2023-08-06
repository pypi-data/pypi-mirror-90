imgflip
=========
A python api to imgflip.


Install
-------
::

  pip install imgflip


How to use?
-----------
::

  python -m imgflip.cli
  python -m imgflip
  imgflip


Development
-----------
setup::

  python -m pip install --upgrade pip wheel setuptools flake8 twine
  python -m pip install -e .

run tests::

  coverage run --source=imgflip -m unittest discover
  coverage report -m

check src::

  flake8 imgflip

check readme::

  python setup.py sdist
  twine check dist/*

make package::

  python setup.py sdist bdist_wheel
  python -m twine upload dist/*

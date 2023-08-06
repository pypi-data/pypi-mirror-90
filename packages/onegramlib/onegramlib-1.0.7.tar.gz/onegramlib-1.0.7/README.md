Python Library for OneGram
===========================

Python 3 library for OneGram!

Installation
------------

Install with `pip`:

    $ sudo apt-get install libffi-dev libssl-dev python-dev
    $ pip3 install onegramlib

Manual installation:

    $ git clone git@gitlab.com:onegram-developers/python-onegramlib.git
    $ cd python-onegramlib
    $ python3 setup.py install --user

Dependencies
------------

Some dependencies are not required for parts of the library to run
properly. However these modules require some additional libraries to be
present:

* `graphenebase.bip38`
   * `pycrypto==2.6.1`
   * `scrypt==0.7.1` (to speedup scrypt hashing)
* `graphenebase.memo`
   * `pycrypto==2.6.1`

Upgrade
-------

    $ pip install --user --upgrade onegramlib

Documentation
-------------

Thanks to readthedocs.io, the documentation can be viewed
[online](http://python-graphenelib.readthedocs.io/en/latest/)

Documentation is written with the help of sphinx and can be compile to
html with:

    cd docs
    make html

Licence
-------

MIT, see `LICENCE.txt`

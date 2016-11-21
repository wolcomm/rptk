.. image:: https://travis-ci.org/wolcomm/rptk.svg?branch=master
    :target: https://travis-ci.org/wolcomm/rptk

==============================
RPTK - Routing Policy Tool Kit
==============================

Python toolkit for prefix filter list management operations
with plugable modules for query and output handling.

Features
========

* Command-line ``rptk`` tool

* Simple python api module

* Query modules:

  * `bgpq3`_ shell wrapper

* Format modules:

  * JSON output
  * IOS classic/XE style prefix-lists

Getting Started
===============

1. Install from pip::
  ``$ pip install rptk``

2. Run bgpq3 installer script::
  ``$ ./install-bgpq3.sh``
  
3. Run tests::
  ``$ python setup.py test``
  
4. Customise defaults in ``rptk.conf``

.. _bgpq3: https://github.com/snar/bgpq3

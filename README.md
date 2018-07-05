<!--description: A python toolkit for prefix filter list management operations. -->
[![image](https://img.shields.io/pypi/v/rptk.svg)](https://pypi.python.org/pypi/rptk)
[![image](https://travis-ci.org/wolcomm/rptk.svg?branch=master)](https://travis-ci.org/wolcomm/rptk)
[![image](https://codecov.io/gh/wolcomm/rptk/branch/master/graph/badge.svg)](https://codecov.io/gh/wolcomm/rptk)
[![Requirements Status](https://requires.io/github/wolcomm/rptk/requirements.svg?branch=master)](https://requires.io/github/wolcomm/rptk/requirements/?branch=master)

# RPTK - Routing Policy Tool Kit

Python toolkit for prefix filter list management operations with
plugable modules for query and output handling.

## Features

  - Command-line `rptk` tool
  - Simple python api module
  - Flask-based web-query api
  - Query modules:
      - native python query module
      - [bgpq3](https://github.com/snar/bgpq3) shell wrapper
  - Format modules
      - JSON output
      - YAML output
      - IOS classic/XE style prefix-lists
      - JunOS prefix-lists
      - BIRD prefix-lists
      - ...more coming soon

## Getting Started

1.  Install from pip:

        $ pip install rptk

2.  Run [bgpq3](https://github.com/snar/bgpq3) installer script, if not
    already installed:

        $ cd $PREFIX/share/rptk/utils/
        $ ./install-bgpq3.sh

3.  Customise settings in `rptk.conf` as necessary:

        $ cd $PREFIX/etc/rptk/
        $ cp rptk.conf.example rptk.conf
        $ vi rptk.conf

4.  Check that test queries are working on the command line:

        $ rptk -F ios -Q bgpq3 AS-WOLCOMM

5.  Check that test queries are working on the web API:

        $ rptk-web
        $ curl http://localhost:8080/ios/AS-WOLCOMM

Refer to
[setup.md](https://github.com/wolcomm/rptk/blob/master/wiki/setup.md)
for addtional steps to setup the online web-api help pages.

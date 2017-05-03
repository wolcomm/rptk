#!/usr/bin/env sh
set -ex
wget https://github.com/snar/bgpq3/archive/v0.1.32.tar.gz
tar -xzvf v0.1.32.tar.gz
cd bgpq3-0.1.32/ && ./configure --prefix=/usr && make && sudo make install
rm v0.1.32.tar.gz

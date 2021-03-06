#!/usr/bin/env sh
# Copyright (c) 2018 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License version 2.0
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
set -ex
wget https://github.com/snar/bgpq3/archive/v0.1.32.tar.gz
tar -xzvf v0.1.32.tar.gz && rm v0.1.32.tar.gz
cd bgpq3-0.1.32/ && ./configure --prefix=/usr && make && sudo make install

#!/usr/bin/env python
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
"""rptk package metadata."""

from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.2.0"
__author__ = "Workonline Communications"
__author_email__ = "communications@workonline.co.za"
__licence__ = "Apache License 2.0"
__copyright__ = "Copyright (c) 2018 Workonline Communications (Pty) Ltd"
__url__ = "https://github.com/wolcomm/rptk"
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet',
]
__entry_points__ = {
    'console_scripts': [
        'rptk=rptk.command_line:main',
        'rptk-web=rptk.web:main'
    ]
}


if __name__ == "__main__":
    print(__version__)

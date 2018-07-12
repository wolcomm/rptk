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
"""rptk web module."""

from __future__ import print_function
from __future__ import unicode_literals

import json

import flask

from rptk import RptkAPI

app = flask.Flask(__name__)


@app.route("/formats")
def get_formats():
    """Return json doc describing the available output formats."""
    opts = flask.request.args.to_dict()
    rptk = RptkAPI(**opts)
    formats = rptk.format_class_loader.class_info
    response = flask.make_response(json.dumps(formats))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/policies")
def get_policies():
    """Return json doc listing the available resolution policies."""
    opts = flask.request.args.to_dict()
    rptk = RptkAPI(**opts)
    policies = rptk.available_policies
    response = flask.make_response(json.dumps(policies))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/<string:format>/<string:obj>")
@app.route("/<string:format>/<string:obj>/<string:policy>")
def get_prefix_list(format=None, obj=None, policy=None):
    """Return prefix-lists for the requested object."""
    opts = flask.request.args.to_dict()
    rptk = RptkAPI(query_policy=policy, format_class_name=format, **opts)
    result = rptk.query(obj=obj)
    output = rptk.format(result=result, name=obj)
    response = flask.make_response(output)
    response.headers['Content-Type'] = rptk.format_class.content_type
    return response


def main():  # pragma: no cover
    """Run the development server."""
    app.run(host='::', port=8080)


if __name__ == "__main__":
    main()

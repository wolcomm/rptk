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

import json

import flask

from rptk import RptkAPI

app = flask.Flask(__name__)


@app.route("/formats")
def get_formats():
    """Return json doc describing the available output formats."""
    opts = flask.request.args.to_dict()
    rptk = RptkAPI(**opts)
    formats = rptk.available_formats()
    response = flask.make_response(json.dumps(formats))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/policies")
def get_policies():
    """Return json doc listing the available resolution policies."""
    opts = flask.request.args.to_dict()
    rptk = RptkAPI(**opts)
    policies = rptk.available_policies()
    response = flask.make_response(json.dumps(policies))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/<string:fmt>/<string:obj>")
@app.route("/<string:fmt>/<string:obj>/<string:policy>")
def get_prefix_list(fmt=None, obj=None, policy=None):
    """Return prefix-lists for the requested object."""
    opts = flask.request.args.to_dict()
    rptk = RptkAPI(object=obj, format=fmt, policy=policy, **opts)
    result = rptk.query()
    response = flask.make_response(result)
    response.headers['Content-Type'] = "text/plain"
    return response


def main():
    """Run the development server."""
    app.run(host='::', port=8080)


if __name__ == "__main__":
    main()

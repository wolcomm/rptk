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
import logging

import flask

from rptk import RptkAPI

app = flask.Flask(__name__)


@app.route("/formats")
def get_formats():
    """Return json doc describing the available output formats."""
    rptk = RptkAPI()
    formats = rptk.format_class_loader.class_info
    response = flask.make_response(json.dumps(formats))
    response.headers['Content-Type'] = "application/json"
    response.headers['Server'] = "rptk-web/{}".format(rptk.version)
    return response


@app.route("/policies")
def get_policies():
    """Return json doc listing the available resolution policies."""
    rptk = RptkAPI()
    policies = rptk.available_policies
    response = flask.make_response(json.dumps(policies))
    response.headers['Content-Type'] = "application/json"
    response.headers['Server'] = "rptk-web/{}".format(rptk.version)
    return response


@app.route("/query")
@app.route("/<string:format>/query")
@app.route("/<string:format>/<string:obj>")
@app.route("/<string:format>/<string:obj>/<string:policy>")
def get_prefix_list(format=None, obj=None, policy=None):
    """Return prefix-lists for the requested object."""
    app.logger.debug(msg="got args: {}".format(flask.request.args))
    objects = flask.request.args.getlist("objects")
    if obj:
        objects.append(obj)
    objects = set(objects)
    if not format:
        format = flask.request.args.get("format")
    if not policy:
        policy = flask.request.args.get("policy")
    rptk = RptkAPI(query_policy=policy, format_class_name=format)
    result = rptk.query(*objects)
    output = rptk.format(result=result)
    response = flask.make_response(output)
    response.headers['Content-Type'] = rptk.format_class.content_type
    response.headers['Server'] = "rptk-web/{}".format(rptk.version)
    return response


def main():  # pragma: no cover
    """Run the development server."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False,
                        help="enable debug mode")
    args = parser.parse_args()
    logger = logging.getLogger()
    for h in app.logger.handlers:
        logger.addHandler(h)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    app.run(host='::', port=8080, debug=args.debug)


if __name__ == "__main__":
    main()

import json
from flask import Flask, request, make_response
from rptk import RptkAPI

app = Flask(__name__)


@app.route("/formats")
def get_formats():
    opts = request.args.to_dict()
    rptk = RptkAPI(**opts)
    formats = rptk.available_formats()
    response = make_response(json.dumps(formats))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/policies")
def get_policies():
    opts = request.args.to_dict()
    rptk = RptkAPI(**opts)
    policies = rptk.available_policies()
    response = make_response(json.dumps(policies))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/<string:fmt>/<string:obj>")
@app.route("/<string:fmt>/<string:obj>/<string:policy>")
def get_prefix_list(fmt=None, obj=None, policy=None):
    opts = request.args.to_dict()
    rptk = RptkAPI(object=obj, format=fmt, policy=policy, **opts)
    result = rptk.query()
    response = make_response(result)
    response.headers['Content-Type'] = "text/plain"
    return response

def main():
    app.run(host='::', port=8080)

if __name__ == "__main__":
    main()

from flask import Flask, request, make_response
from rptk import RptkAPI

app = Flask(__name__)


@app.route("/formats")
def get_formats():
    opts = request.args.to_dict()
    rptk = RptkAPI(**opts)
    formats = rptk.available_formats()
    response = make_response("\n".join(formats))
    response.headers['Content-Type'] = "text/plain"
    return response


@app.route("/<string:fmt>/<string:obj>")
def get_prefix_list(fmt=None, obj=None):
    opts = request.args.to_dict()
    rptk = RptkAPI(object=obj, format=fmt, **opts)
    result = rptk.query()
    response = make_response(result)
    response.headers['Content-Type'] = "text/plain"
    return response

if __name__ == "__main__":
    app.run(host='::', port=8080)

from flask import Flask, request, make_response
from rptk.api import Rptk

app = Flask(__name__)


@app.route("/<string:fmt>/<string:obj>")
def get(fmt=None, obj=None):
    opts = request.args.to_dict()
    rptk = Rptk(object=obj, format=fmt, **opts)
    result = rptk.query()
    response = make_response(result)
    response.headers['Content-Type'] = "text/plain"
    return response

if __name__ == "__main__":
    app.run(host='::', port=8080)

from flask_api import FlaskAPI
from rptk.api import Rptk

app = FlaskAPI(__name__)


@app.route("/<string:format>/<string:obj>", methods=['GET'])
def get(format=None, obj=None):
    rptk = Rptk(object=obj, format=format)
    result = rptk.query()
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

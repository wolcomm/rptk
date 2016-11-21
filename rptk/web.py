from flask_api import FlaskAPI
from flask_api.renderers import BaseRenderer, BrowsableAPIRenderer
from flask_api.decorators import set_renderers
from rptk.api import Rptk

app = FlaskAPI(__name__)


class TextRenderer(BaseRenderer):
    media_type = 'text/plain'

    def render(self, data, media_type, **options):
        return "%s\n" % data


@app.route("/<string:fmt>/<string:obj>", methods=['GET'])
@set_renderers(TextRenderer)
def get(fmt=None, obj=None):
    rptk = Rptk(object=obj, format=fmt)
    result = rptk.query()
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

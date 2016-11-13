import logging
from flask import jsonify
from flask import Flask
from scorehub.parsers import ParserFactory

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_scores_for(name):
    parser = ParserFactory.make_parser(name)
    return parser.get_scores_json()


@app.route('/')
def index():
    return jsonify({
        'status': 200,
        'message': 'All systems go'
    })


@app.route('/ncaaf')
def ncaaf():
    logger.debug('\tRequest for NCAA Football scores received')
    try:
        return jsonify(get_scores_for('ncaaf')), 200
    except Exception as e:
        logger.error(e)
        return jsonify({
            'status': 500,
            'message': 'Something weng wrong'
        })


if __name__ == '__main__':
    app.run(debug=True)

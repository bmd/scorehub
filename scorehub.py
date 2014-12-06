import logging
import json

from flask import Flask
from flask.ext.cacheify import init_cacheify
from score_parsers import get_ncaaf_scores


app = Flask(__name__)
### Define application-level variables
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
cache = init_cacheify(app)


def check_cache(key):
    c = cache.get(key)
    return c


def get_scores_generic(name, score_callback):
    ### Caching when I get to it
    scores = check_cache(name)
    if not scores:
        logger.debug('\t -> No cached value found: requesting new results...')
        scores = score_callback()
        logger.debug('\t -> Setting value in cache.')
        cache.set(name, scores, 5 * 60)
    else:
        logger.debug('\t -> Value found in cache: returning...')
    return scores


@app.route('/')
def index():
    return 'This is the homepage. The repository for this app is at <a href="//github.com/bmd/cfb-scores">github</a>', 200


@app.route('/ping')
def ping():
    """ Just do something that returns a 200 """
    return '200: Nothing to see here. Go away.', 200


@app.route('/ncaaf')
def ncaaf():
    logger.debug('\t Request for NCAA Football scores received')
    # parse scores
    try:
        logger.debug('\t -> Dispatching request to score generic')
        scores = get_scores_generic('ncaaf', get_ncaaf_scores)
        logger.debug('\t -> Score feed parsed successfully. Returning results object.')
        return json.dumps(scores), 200
    # handle errors
    except Exception as e:
        logger.error(e)
        return 'Something went wrong -- internal error.', 500


if __name__ == '__main__':

    app.run(debug=True)

import logging
import json

from flask import Flask

from score_parsers import get_ncaaf_scores


app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

def get_scores_generic(name, score_callback):
    scores = score_callback()
    ### Caching when I get to it
    #scores = check_cache(name)
    #if not scores:
    #    scores = score_callback()
    #    set_cache(name, scores)
    return scores

@app.route('/ping')
def ping():
    """ Just do something that returns a 200 """
    return '200: Nothing to see here. Go away.', 200

@app.route('/ncaaf')
def ncaaf():
    try:
        scores = get_scores_generic('ncaaf', get_ncaaf_scores)
        return json.dumps(scores), 200
    except:
        return 'Something went wrong -- internal error.', 500


if __name__ == '__main__':
    app.run(debug=True)

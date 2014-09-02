from app import app  #comment out to run on PyAW
import sqlite3 as sqlite
from flask import render_template, abort
import unicodecsv as csv
from collections import OrderedDict
import json
import pyBL.pyBL.ncf as ncf

# Uncomment to run App on Python Anywhere
#from flask import Flask
#import csv
#app = Flask(__name__)
#DATABASE = '/home/bmaionedowning/mysite/travelers.sqlite'

#DATABASE = 'travelers.sqlite' #comment out to run on PyAW


@app.route('/')
@app.route('/index/')
def index():
    g1, g2, g3 = ncf.get_ncaaf_scores()
    return render_template("games.html",
        to_play=g1, in_progress=g2, done=g3,
        title="This Week's Games")

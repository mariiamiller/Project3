import os
import glob
import pandas as pd
import numpy as np
import requests
import time
import csv
import json
import datetime
from bs4 import BeautifulSoup
import librosa
from tensorflow.keras.models import load_model
import librosa
import librosa.display
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.utils import to_categorical
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, redirect, request
# from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///earnings.sqlite"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# #Samples_Metadata = Base.classes.sample_metadata
# Earnings = Base.classes.Earnings

# engine = create_engine("sqlite:///db/earnings.sqlite")

# Base = automap_base()

# Base.prepare(engine, reflect=True)

# Earnings = Base.classes.earnings
# symbols = Base.classes.symbols_sectors
# q3earnings = Base.classes.earnings_dates
# surprise_sum = Base.classes.surprise_summary_clean

print("test1")
#db = PyMongo(app, uri="mongodb://localhost:27017/songs_db")
client = MongoClient(port=27017)
db = client.songs_db
def extract_max(pitches,magnitudes, shape):
    new_pitches = []
    new_magnitudes = []
    for i in range(0, shape[1]):
        new_pitches.append(np.max(pitches[:,i]))
        new_magnitudes.append(np.max(magnitudes[:,i]))
    return (new_pitches,new_magnitudes)


# label_dic = {0: '_amazing_grace_elvis',
 	# 1: '_hallelujah',
 	# 2: '_hush_little_baby',
 	# 3: '_i_want_it_that_way',
 	# 4: '_l_o_v_e',
 	# 5: '_over_the_rainbow',
 	# 6: '_row_row_row_your_boat',
 	# 7: '_star_spangled_whitney',
	# 8: '_the_alphabet_song',
	# 9: '_twist_and_shout'}

label_dic = {0: '_amazing_grace_elvis',
 	1: '_hallelujah',
 	#2: '_hush_little_baby',
 	2: '_i_want_it_that_way',
 	3: '_l_o_v_e',
 	4: '_over_the_rainbow',
 	5: '_row_row_row_your_boat',
 	6: '_star_spangled_whitney',
	7: '_the_alphabet_song',
	8: '_twist_and_shout'}
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/postblob", methods=['POST'])
def post():
	file = request.files['file']
	path='static/audiofiles'
	#root = r'/Users/mariamiller/Documents/project3'
	dt = datetime.datetime.now()
	fileFullPath = r'%s/%s.wav' % (path, dt.strftime("%Y%m%d-%H%M%S%f")[:-3] )
	file.save(fileFullPath)
	return "Hello"

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
	path='static/audiofiles/'
	#root = r'/Users/mariamiller/Documents/project3'
	list_of_files = glob.glob(path + '*') # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	#latest_file = path + '20191220-012137005.wav'
	y,sr = librosa.load(latest_file)
	#y = np.tile(y,4)
	#y = y[:sr*60]
	y = np.tile(y,2)
	y = y[:sr*20]
	sg0 = librosa.stft(y)
	sg_mag, sg_phase = librosa.magphase(sg0)
	sg1 = librosa.feature.melspectrogram(S=sg_mag, sr = sr)
	sg2 = librosa.amplitude_to_db(sg1, ref=np.min)
	sg2 = (np.expand_dims(sg2,0))
	path2='static/models/songs525/'
	model=load_model(path2+'songs525_9.h5')
	#df=pd.read_csv(path2+'megamodel_labels.csv')

	encoded_prediction = int(model.predict_classes(sg2))
	song = label_dic[int(encoded_prediction)]
	result = db.songs_links.find_one({'songid':song})
	embed_link = 'https://www.youtube.com/embed/'+ result['song_youtube_link'].split('=')[-1]
	return jsonify([result['song_name'],result['song_description'],result['song_youtube_link'],embed_link])



# @app.route("/names/<symbol>")
# def names(symbol):
#     """Return a list of names and info."""

#     # # Use Pandas to perform the sql query
#     # stmt = db.session.query(symbol).statement
#     # df = pd.read_sql_query(stmt, db.session.bind)

#     # # Return a list of the column names (sample names)
#     # return jsonify(list(df.columns)[2:])

#     session = Session(engine)

#     results = session.query(symbols.symbol, symbols.Name, symbols.sector, symbols.industry, symbols.SummaryQuote).\
#     filter(symbols.symbol == symbol).all()

#     #session.close()
#     all_symbols = list(np.ravel(results))

#     return jsonify(all_symbols)




if __name__ == "__main__":
    app.run(debug=True)

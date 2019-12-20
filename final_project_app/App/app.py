import os

import pandas as pd
import numpy as np
import requests
import time
import csv
import json
from bs4 import BeautifulSoup
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

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
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")





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
    app.run()

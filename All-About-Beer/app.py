# import necessary libraries
# from models import create_classes
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# engine = create_engine('postgres://njvrdjyvjmdbff:8574a3313def94cb7b048ef3496350a723d4ebcbb2ae1a709d66a79eab0112fe@ec2-54-211-77-238.compute-1.amazonaws.com:5432/d7ne1s21u49i5u')

# Base = automap_base()
# Base.prepare(engine, reflect=True)

# Save references to each table
# Income = Base.classes.income
# Crime = Base.classes.crime
# Ethnicity = Base.classes.ethnicity
# Restaurant = Base.classes.restaurant
# NeighbourhoodRestaurant = Base.classes.neighbourhood_restaurant


#################################################
# Flask Routes
#################################################


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/recommend_a', methods=['GET', 'POST'])
def recommend_a():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('reco-sys-a.html')


if __name__ == "__main__":
    app.run(debug=True)

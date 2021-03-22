# import necessary libraries
# from models import create_classes
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import pandas as pd
import numpy as np
import requests
from django.shortcuts import render
# import pickle

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Load the model
# model = pickle.load(open('model.pkl', 'rb'))

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

# ML
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error

# MSE calculates the difference between our predicted and actual ratings
def get_mse(pred, actual):
    # Extract only real userId with ratings
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return mean_squared_error(pred, actual)


# Applies only to Beer Top_N that has similar similarity to a specific beer -> Takes a long time
def predict_rating_topsim(ratings_arr, item_sim_arr, n=20):
    # Initialize a prediction matrix filled with zeros equal to the size of the user-item rating matrix
    pred = np.zeros(ratings_arr.shape)

    # Loop as many beers in the user-item rating matrix
    for col in range(ratings_arr.shape[1]):
        # Return the indices of n data matrices in the order of similarity in the similarity matrix
        top_n_items = [np.argsort(item_sim_arr[:, col])[:-n - 1:-1]]
        # Personalized prediction score calculation: For each col beer (1 piece), the prediction score of 3015 users
        for row in range(ratings_arr.shape[0]):
            pred[row, col] = item_sim_arr[col, :][top_n_items].dot(
                ratings_arr[row, :][top_n_items].T)
            pred[row, col] /= np.sum(item_sim_arr[col, :][top_n_items])

    return pred

# Recommend a beer that users haven't tasted before.
def get_not_tried_beer(ratings_matrix, userId):
    # Extracts all beer information of the user entered as userId and returns it to Series
    # The returned user_rating is a Series object with the userId as an index.
    user_rating = ratings_matrix.loc[userId, :]

    # If user_rating is greater than 0, it is related to the existing movie.
    # Extract target index and make list object
    tried = user_rating[user_rating > 0].index.tolist()

    # Make all beer names into list objects
    beer_list = ratings_matrix.columns.tolist()

    # Movies corresponding to tried as a list comprehension are excluded from beer_list
    not_tried = [beer for beer in beer_list if beer not in tried]

    return not_tried

# After extracting the user id index and the beer name entered as not_tried from the predicted rating DataFrame
# Sort by highest predicted rating
def recomm_beer_by_userid(pred_df, userId, not_tried, top_n):
    recomm_beer = pred_df.loc[userId, not_tried].sort_values(ascending=False)[:top_n]
    return recomm_beer

# Calculate similarity after selecting a feature among Rating, Aroma, Flavor, and Mouthfeel
def recomm_feature(df, col):
    feature = col
    ratings = df[['user','beer_name', feature]]

    # User-ID matrix composition using pivot table
    ratings_matrix = ratings.pivot_table(feature, index='user', columns='beer_name')
    ratings_matrix.head(3)
    # Nan processing using fillna function
    ratings_matrix = ratings_matrix.fillna(0)

    # Transpose to calculate similarity
    ratings_matrix_T = ratings_matrix.transpose()

    # Finding cosine similarity from item-user matrix
    item_sim = cosine_similarity(ratings_matrix_T, ratings_matrix_T)

    # Convert the beer name to DataFrame by mapping the beer name to the NumPy matrix returned by cosine_similarity()
    item_sim_df = pd.DataFrame(data=item_sim, index=ratings_matrix.columns,
                              columns=ratings_matrix.columns)

    return item_sim_df

# Recommend 5 similar similarities to the beer
def recomm_beer(item_sim_df, beer_name):
    # Recommended only 5 beers with a high similarity
    return item_sim_df[beer_name].sort_values(ascending=False)[1:4]


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
        beer_name = request.form["beerName"]
        factor = request.form["selectedFactor"]

        # call from RDS with beer and factors (call using SQLAlchemy)
        print(beer_name)
        print(factor)
        beer_list = pd.read_csv('beer.csv', encoding='utf-8', index_col=0)
        ratings = pd.read_csv('Ratings.csv', encoding='utf-8', index_col=0)
        beer_list = beer_list['beer_name']
        df_aroma = recomm_feature(ratings, 'Aroma')
        df_flavor = recomm_feature(ratings, 'Flavor')
        df_mouthfeel = recomm_feature(ratings, 'Mouthfeel')
        if factor == 'Aroma':
            df = df_aroma*0.8 + df_flavor*0.1 + df_mouthfeel*0.1
        if factor == 'Flavor':
            df = df_aroma*0.1 + df_flavor*0.8 + df_mouthfeel*0.1
        if factor == 'Mouthfeel':
            df = df_aroma*0.1 + df_flavor*0.1 + df_mouthfeel*0.8
        result = recomm_beer(df, beer_name)
        result = result.index.tolist()
        print(result)
        return render_template('templates/reco-sys-a.html',result = result)
                #    {'result':result, 'beer_list':beer_list})
        # output from  code goes into another table called webapptransactions

        # the redirect can be to the same route or somewhere else
       # return redirect(url_for('recommend_a')) ## pulls API endpoint that pulls the latestet info from the db
        # requests.Response(url_for('reco-sys-a_test.html'),
        #            {'result':result})
    # show the form, it wasn't submitted
    # return render_template('reco-sys-a.html')

@app.route('/api/beer')
def api_index(): 
    # search from webapp transactions latest record 
    return jsonify(latest_record)

@app.route('/recommend_b', methods=['GET', 'POST'])
def recommend_b():
    if request.method == 'POST':
        # do stuff when the form is submitted


        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('reco-sys-b.html')

# @app.route('/api',methods=['POST'])
# def predict():
#     # Get the data from the POST request.
#     data = request.get_json(force=True)
#     # Make prediction using model loaded from disk as per the data.
#     prediction = model.predict([[np.array(data['exp'])]])
#     # Take the first value of prediction
#     output = prediction[0]
#     return jsonify(output)

# Query the database and send the jsonified results
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     if request.method == "POST":
#         name = request.form["petName"]
#         lat = request.form["petLat"]
#         lon = request.form["petLon"]

#         pet = Pet(name=name, lat=lat, lon=lon)
#         db.session.add(pet)
#         db.session.commit()
#         return redirect("/", code=302)

#     return render_template("form.html")


# @app.route("/api/pals")
# def pals():
#     results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

#     hover_text = [result[0] for result in results]
#     lat = [result[1] for result in results]
#     lon = [result[2] for result in results]

#     pet_data = [{
#         "type": "scattergeo",
#         "locationmode": "USA-states",
#         "lat": lat,
#         "lon": lon,
#         "text": hover_text,
#         "hoverinfo": "text",
#         "marker": {
#             "size": 50,
#             "line": {
#                 "color": "rgb(8,8,8)",
#                 "width": 1
#             },
#         }
#     }]

#     return jsonify(pet_data)



if __name__ == "__main__":
    app.run(debug=True)
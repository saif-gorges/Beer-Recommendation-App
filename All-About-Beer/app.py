# import necessary libraries
# from models import create_classes
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import psycopg2
from flask import Flask, render_template, jsonify, request, redirect, url_for #, Resource
from flask_sqlalchemy import SQLAlchemy
#from flask_pymongo import PyMongo

import pandas as pd
import numpy as np

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# server = "beers-data.cgl0jpbw6pfo.ca-central-1.rds.amazonaws.com"
# database = "beers-data"
# port = "5432"
# username = "root"
# password = "teamawesome"
# conn = f"postgres://{username}:{password}@{server}:{port}/{database}"
# engine = create_engine(conn, echo=False)

# Upload and read CSV using Python Flask
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# class UploadCSV(Resource):

#     def post(self):
#         files = request.files['files']
#         files.save(os.path.join(ROOT_PATH,files.filename))
#         data = pd.read_csv(os.path.koin(ROOT_PATH,files.filename))
#         print(data)

# api.add_resource(UploadCSV, '/v1/upload')

# if __name__ =='__main__':
#     app.run(host='localhost', debug=True, port=5000)


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
        # Receives input from the front from POST
        beer_name = request.form["beerName"]
        factor = request.form["selectedFactor"]

        # call from RDS with beer and factors (call using SQLAlchemy)
        #Print the results from POST
        # print(beer_name)
        # print(factor)

        # Read Beer-Ratings file which has User's Aroma, Flavor, Mouthfeel ratings
        ratings = pd.read_csv("./All-About-Beer/data/final_data/final_data_3.csv", encoding='unicode_escape',index_col=0)
        #print(ratings)

        # Calculate the logic corresponding to the recommendation system using recomm_feature defined function.
        df_aroma = recomm_feature(ratings, 'aroma')
        df_flavor = recomm_feature(ratings, 'flavor')
        df_mouthfeel = recomm_feature(ratings, 'mouthfeel')
        if factor == 'Aroma':
            df = df_aroma*0.8 + df_flavor*0.1 + df_mouthfeel*0.1
        if factor == 'Flavor':
            df = df_aroma*0.1 + df_flavor*0.8 + df_mouthfeel*0.1
        if factor == 'Mouthfeel':
            df = df_aroma*0.1 + df_flavor*0.1 + df_mouthfeel*0.8

        results = recomm_beer(df, beer_name)
        results = results.index.tolist()
        #print(results)

        # Initialize the list for the dictionary of beer names
        beer_data = {
            'beer_name': results
        }
        #print(beer_data)
        return render_template('reco-sys-a-result.html', beer_data=beer_data)
    return render_template('reco-sys-a.html')

@app.route('/api/beer')
def api_index(): 
    # search from webapp transactions latest record 
    return jsonify(latest_record)

@app.route('/recommend_b', methods=['GET', 'POST'])
def recommend_b():

    ratings = pd.read_csv("./All-About-Beer/data/final_data/final_data_3Copy.csv", encoding='unicode_escape',index_col=0)

    if request.method == 'POST':
        # do stuff when the form is submitted
        beer = []
        rating = []

        for i in range(1, 6):
            name = request.form["name"]
            beer_name = request.form[f"beer{i}"]
            beer.append(beer_name)
            rate = request.form[f"rate{i}"]
            rating.append(rate)

        for i in range(len(beer)):
            tmp = []
            tmp.append(name)
            tmp.append(beer[i])
            tmp.append(float(rating[i]))
            tmp = pd.DataFrame(data=[tmp], columns=['user','beer_name','rating'])
            # tmp = pd.DataFrame(data=[tmp], columns=['beer_name','rating'])
            ratings = pd.concat([ratings, tmp])

        uname = name
        ratings_matrix = ratings.pivot_table('rating', index='user', columns='beer_name')
        ratings_matrix = ratings_matrix.fillna(0)
        ratings_matrix_T = ratings_matrix.transpose()

        item_sim = cosine_similarity(ratings_matrix_T, ratings_matrix_T)
        item_sim_df = pd.DataFrame(data=item_sim, index=ratings_matrix.columns,
                                   columns=ratings_matrix.columns)
        
        # Only users similar to top_n are used for recommendation.
        ratings_pred = predict_rating_topsim(ratings_matrix.values, item_sim_df.values, n=5)
        # The calculated predicted score data is recreated as a DataFrame.
        ratings_pred_matrix = pd.DataFrame(data=ratings_pred, index=ratings_matrix.index,
                                           columns=ratings_matrix.columns)   

        # Extracting the beer name that the user did not tasted
        not_tried = get_not_tried_beer(ratings_matrix, uname)

        # Recommended beer as an item-based nearest neighbor CF
        recomm_beer = recomm_beer_by_userid(ratings_pred_matrix, uname, not_tried, top_n=3)
        recomm_beer = pd.DataFrame(data=recomm_beer.values, index=recomm_beer.index,
                                   columns=['Prediction score'])
        # Extract only the beer name from the recommendation
        result = recomm_beer.index.tolist()  
        beer_result = {
            'beer_name': result
            }
        # print(beer_result)
        return render_template('reco-sys-b-result.html', beer_result=beer_result)
    return render_template('reco-sys-b.html')

if __name__ == "__main__":
    app.run(debug=True)

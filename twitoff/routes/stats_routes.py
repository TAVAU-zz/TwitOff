from flask import Blueprint, request, jsonify, render_template

from sklearn.linear_model import LogisticRegression # for example

from twitoff.models import User, Tweet
# from .services.basilica_service import basilica_api_client

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'elonmusk', 'screen_name_b': 's2t2', 'tweet_text': 'Example tweet text here'}
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print("-----------------")
    print("FETCHING TWEETS FROM THE DATABASE...")
   
    #TODO

    print("-----------------")
    print("TRAINING THE MODEL...")
    
    classifier = LogisticRegression()
    # TODO: classifier.fit(___________, ___________)

    print("-----------------")
    print("MAKING A PREDICTION...")

    # TODO
    
    return render_template("results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely="TODO" 
    )
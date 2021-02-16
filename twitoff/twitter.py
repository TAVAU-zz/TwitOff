"""
Retrieve Tweets, embeddings, and persist in the database.
"""
from os import getenv
import spacy
import tweepy
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_CONSUMER_KEY'),
                                   getenv('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(getenv('TWITTER_ACCESS_TOKEN'),
                                   getenv('TWITTER_ACCESS_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

# nlp model
nlp = spacy.load('my_model')
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(username):
    """
    Add or update a user *and* their Tweets, error if no/private user.
    """
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, 
                                        tweet_mode='extended', since_id=db_user.newest_tweet_id)
        
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # Get embedding for tweet, and store in db
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet) 
    except Exception as e:
        print('Error preocessing{}: {}'.format(username,e))
        raise e
    else: # hit here when pass try
        DB.session.commit()

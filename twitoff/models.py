"""SQLAlchemy module for TwitOff."""
from flask_sqlalchemy import SQLAlchemy
# from .twitter import add_or_update_user

DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users that we pull and analyze Tweets for."""
    id = DB.Column(DB.Integer, primary_key=True) # id column (primary key)
    name = DB.Column(DB.String(15), nullable=False) # name column
    newest_tweet_id = DB.Column(DB.BigInteger) # keeps track of recent tweet

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Tweet(DB.Model):
    """Tweet text data - associated with Users Table"""
    id = DB.Column(DB.BigInteger, primary_key=True) # id column (primary key)
    text = DB.Column(DB.Unicode(300))
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)
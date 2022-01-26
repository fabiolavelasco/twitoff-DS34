from flask_sqlalchemy import SQLAlchemy

# Create a DB object
DB = SQLAlchemy()

# Create a table with a specific schema
# We will do that by creating a python class


class User(DB.Model):
    # Two columns inside our user table
    # ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # Username columns schema
    username = DB.Column(DB.String, nullable=False)
    # Tweets list is created by the .relationship and the backref in the Tweet class
    # Tweets = []
    newest_tweet_id = DB.Column(DB.BigInteger)


class Tweet(DB.Model):
    # ID columns schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # Text columns schema
    text = DB.Column(DB.Unicode(300), nullable=False)
    # User columns schema (secondary/foreign key)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    # Set up a relationship between the tweets and the users
    # will automarically create the one-to-many relationship, but also add a new attribute
    # onto the "user" called "tweets" which will be a lost of all the user tweets
    user = DB.relationship("User", backref=DB.backref('tweets'), lazy=True)

    # Word Embedings Vector Storage (vector for short)
    vect = DB.Column(DB.PickleType, nullable=False)

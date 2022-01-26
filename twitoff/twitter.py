from os import getenv
import tweepy
from .models import DB, Tweet, User
import spacy


# Get our API keys from our .env file
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to Twitter API
# Authenticate
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
# Open a connection to the API
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    try:
        twitter_user = TWITTER.get_user(screen_name=username)

        # Is this twitter user already in our DB?
        # If so, then just update their tweet information
        # Don't create totally new user
        db_user = (User.query.get(twitter_user.id) or User(
            id=twitter_user.id, username=username))

        DB.session.add(db_user)

        # Get all of user's tweets if they're a new user
        # Get only yheir most recent tweets
        # if the user is already int he DB
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True,
            include_rts=False, tweet_mode='extended',
            since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # Loop over the tweets and insert then intot he DB
        # one by one
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id, text=tweet.full_text[:300],
                user_id=db_user.id,
                vect=tweet_vector)

            DB.session.add(db_tweet)
    except Exception as error:
        print(f'Error when processing {username}: {error}')
        raise error
    else:
        # Commit (save) the DB session
        DB.session.commit()


nlp = spacy.load('my_model/')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

from flask import Flask, render_template
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user


def create_app():
    app = Flask(__name__)

    # Configuration variable to our app
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect our database to the app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        # query for all users in the database
        users = User.query.all()
        print(users)
        return render_template('base.html', title='Home', users=users)

    @app.route('/populate')
    # Test my dataset functionality
    # by inserting some fake data into the DB
    def populate():

        # Make two new users
        add_or_update_user('ryanallred')
        add_or_update_user('nasa')
        add_or_update_user('nihilist_ds')

        return render_template('base.html', title='Populate')

    @app.route('/update')
    # Test my database functionality
    # by inserting some fake data into the DB
    def update():

        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Update User Tweets')

    @app.route('/reset')
    def reset():
        # Do some dataset stuff
        # Drop old DB tables
        # Remake new DB tables
        # Remove everything from the DB
        DB.drop_all()
        # Recreate the User and Tweet tables
        # so that they're ready to be used (inserted into)
        DB.create_all()
        return render_template('base.html', title='Reset database')

    return app


def get_usernames():
    # get all usernames of existing users
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)
    return usernames

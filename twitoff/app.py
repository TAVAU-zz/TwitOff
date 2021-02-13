"""
Main application and routing logic for TwitOff.
"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"# getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = getenv('ENV') # TODO change before deploying 'debug'
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])
    
    @app.route('/user/<name>')
    def update(name):
        add_or_update_user(name)
        return render_template('base.html', title='Home', users=User.query.all())

    return app
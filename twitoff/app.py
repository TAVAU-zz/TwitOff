"""
Main application and routing logic for TwitOff.
"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .routes.stats_routes import stats_routes
import logging

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"# getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = getenv('ENV') # TODO change before deploying 'debug'
    DB.init_app(app)
    app.register_blueprint(stats_routes)
    gunicorn_logger = logging.getLogger('gunicorn.error')

    @app.route('/')
    def index():
        return render_template('prediction_form.html')
    
    @app.route('/root')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def update(name=None):
        message='' 
        # import pdb; pdb.set_trace()
        name = name or request.values['user_name']
        tweets = []
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
                tweets = User.query.filter(User.name == name).one().tweets# one() throw erroe, first() return none
        except Exception as e:
            message= 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    return app
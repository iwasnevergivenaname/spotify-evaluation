from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config


def create_app():
	"""create flask application"""
	app = Flask(__name__, instance_relative_config=False)
	# app.config.from_object('config.Config')
	app.config.from_object(config)
	db = SQLAlchemy(app)
	
	with app.app_context():
		# import parts of our application
		from .home import home
		from .profile import profile
		from .spotify_auth import spotify_auth
		from .search import search
		from .track_details import track_details
		from .artist_details import artist_details
		from .about import about
		from .predict import predict
		from .evaluation import evaluation
		
		# register blueprints
		app.register_blueprint(home.home_bp)
		app.register_blueprint(profile.profile_bp)
		app.register_blueprint(spotify_auth.spotify_auth_bp)
		app.register_blueprint(search.search_bp)
		app.register_blueprint(track_details.track_details_bp)
		app.register_blueprint(artist_details.artist_details_bp)
		app.register_blueprint(about.about_bp)
		app.register_blueprint(predict.predict_bp)
		app.register_blueprint(evaluation.evaluation_bp)
		
		return app

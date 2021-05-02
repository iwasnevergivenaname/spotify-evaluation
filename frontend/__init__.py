from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import config
import commands
from models import connect_db, db


def create_app():
	"""create flask application"""
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object(config)
	# db = SQLAlchemy(app)
	connect_db(app)
	db.create_all()
	
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
		from .saved_evaluations import saved_evaluations
		from .error import error
		
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
		app.register_blueprint(saved_evaluations.saved_evaluations_bp)
		app.register_blueprint(error.error_bp)
		
		return app

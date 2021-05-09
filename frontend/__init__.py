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
	# db.create_all()
	
	with app.app_context():
		# import parts of our application
		from .static_pages import static_pages
		from .spotify_api import spotify_api
		from .prediction import prediction
		
		# register blueprints
		app.register_blueprint(static_pages.static_pages_bp)
		app.register_blueprint(spotify_api.spotify_api_bp)
		app.register_blueprint(prediction.prediction_bp)
		
		return app

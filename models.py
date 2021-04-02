from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
	"""Connect to database."""
	
	db.app = app
	db.init_app(app)


class User(db.Model):
	"""User"""
	
	__tablename__ = "users"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String, nullable=False)
	
	# genres = db.relationship("Genre", backref="user")


class Artist(db.Model):
	"""Artist"""
	
	__tablename__ = "artists"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String, nullable=False, unique=True)
	popularity = db.Column(db.Integer, nullable=False)
	image = db.Column(db.String)
	
	# genres = db.relationship("Genre", backref="artist")
	# track = db.relationship('AudioFeatures')

class AudioFeatures(db.Model):
	"""Audio Features for a Track"""
	
	__tablename__ = "audio features"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	track_name = db.Column(db.String, nullable=False)
	# artist_id = db.Column(db.ForeignKey('artist.id'), nullable=False)
	popularity = db.Column(db.Integer, nullable=False)
	energy = db.Column(db.Float, nullable=False)
	dance = db.Column(db.Float, nullable=False)
	acoustic = db.Column(db.Float, nullable=False)
	speech = db.Column(db.Float, nullable=False)
	valence = db.Column(db.Float, nullable=False)
	
	# artist = db.relationship('Artist')


class Genre(db.Model):
	"""Genre"""
	
	__tablename__ = "genres"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String, nullable=False, unique=True)
	# artist_id = db.Column(db.ForeignKey('artist.id'), nullable=False)
	# user_id = db.Column(db.ForeignKey('user.id'), nullable=False)


class Evaluation(db.Model):
	"""Evaluation"""
	
	__tablename__ = "evaluations"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	# user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
	result = db.Column(db.String, nullable=False)
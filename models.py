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
	spotify_id = db.Column(db.String, nullable=False, unique=True)
	

class Artist(db.Model):
	"""Artist"""
	
	__tablename__ = "artists"
	
	id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
	name = db.Column(db.String, nullable=False, unique=True)
	popularity = db.Column(db.Integer)
	image = db.Column(db.String)


class Track(db.Model):
	"""Audio Features for a Track"""
	
	__tablename__ = "tracks"
	
	id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
	title = db.Column(db.String, nullable=False)
	artist_id = db.Column(db.Text, db.ForeignKey('artists.id'), nullable=False)
	popularity = db.Column(db.Integer, nullable=False)
	energy = db.Column(db.Float, nullable=False)
	dance = db.Column(db.Float, nullable=False)
	acoustic = db.Column(db.Float, nullable=False)
	speech = db.Column(db.Float, nullable=False)
	valence = db.Column(db.Float, nullable=False)
	image = db.Column(db.String)
	
	artist = db.relationship('Artist')

class Evaluation(db.Model):
	"""Evaluation"""
	
	__tablename__ = "evaluations"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Text, db.ForeignKey('users.spotify_id'), nullable=False)
	result = db.Column(db.String)
	message = db.Column(db.String)
	track_id = db.Column(db.Text, db.ForeignKey('tracks.id'), nullable=False)
	
	user = db.relationship('User')
	track = db.relationship('Track')

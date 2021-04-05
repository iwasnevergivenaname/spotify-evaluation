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
	
	# genres = db.relationship("Genre", backref="user")


class Artist(db.Model):
	"""Artist"""
	
	__tablename__ = "artists"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String, nullable=False, unique=True)
	popularity = db.Column(db.Integer)
	image = db.Column(db.String)
	spotify_id = db.Column(db.String, nullable=False, unique=True)
	
	# genres = db.relationship("Genre", backref="artist")
	tracks = db.relationship('Track')


class Track(db.Model):
	"""Audio Features for a Track"""
	
	__tablename__ = "tracks"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String, nullable=False)
	artist_id = db.Column(db.Text, db.ForeignKey('artists.spotify_id'), nullable=False)
	popularity = db.Column(db.Integer, nullable=False)
	energy = db.Column(db.Float, nullable=False)
	dance = db.Column(db.Float, nullable=False)
	acoustic = db.Column(db.Float, nullable=False)
	speech = db.Column(db.Float, nullable=False)
	valence = db.Column(db.Float, nullable=False)
	spotify_id = db.Column(db.String, nullable=False, unique=True)
	
	artist = db.relationship('Artist')


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
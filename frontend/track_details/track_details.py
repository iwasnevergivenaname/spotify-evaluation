from flask import render_template, Blueprint, session, redirect
from flask import current_app as app
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from models import Track, Artist, connect_db, db

# blueprint configuration
track_details_bp = Blueprint(
	'track_details_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"


@track_details_bp.route("/track/<track_id>", methods=["GET"])
def track_details(track_id):
	# access token to access api
	access_token = session['access_token']
	auth_header = {"Authorization": f"Bearer {access_token}"}
	
	# track
	track_endpoint = f"{spotify_api_url}/tracks/{track_id}"
	track_resp = requests.get(track_endpoint, headers=auth_header)
	track_data = json.loads(track_resp.text)
	
	# track features like popularity and valence
	track_features_endpoint = f"{spotify_api_url}/audio-features/{track_id}"
	track_features_resp = requests.get(track_features_endpoint, headers=auth_header)
	track_features_data = json.loads(track_features_resp.text)
	
	default = 0.00
	
	title = track_data['name']
	artist_id = track_data['artists'][0]['id']
	popularity = track_data['popularity']
	
	if not track_features_data.get('energy'):
		energy = default
	else:
		energy = track_features_data['energy']
	
	if not track_features_data.get('danceability'):
		dance = default
	else:
		dance = track_features_data['danceability']
	
	if not track_features_data.get('acousticness'):
		acoustic = default
	else:
		acoustic = track_features_data['acousticness']
	
	if not track_features_data.get('speechiness'):
		speech = default
	else:
		speech = track_features_data['speechiness']
	
	if not track_features_data.get('valence'):
		valence = default
	else:
		valence = track_features_data['valence']
	
	spotify_id = track_features_data['id']
	
	if Artist.query.get(artist_id) and Track.query.get(spotify_id):
		pass
	elif Artist.query.get(artist_id) and not Track.query.get(spotify_id):
		track = Track(title=title, artist_id=artist_id, popularity=popularity, energy=energy, dance=dance,
		              acoustic=acoustic, speech=speech, valence=valence, id=spotify_id)
		db.session.add(track)
		db.session.commit()
	else:
		name = track_data['artists'][0]['name']
		spotify_id = track_data['artists'][0]['id']
		
		artist = Artist(name=name, id=spotify_id)
		db.session.add(artist)
		db.session.commit()
		
		track = Track(title=title, artist_id=artist_id, popularity=popularity, energy=energy, dance=dance,
		              acoustic=acoustic, speech=speech, valence=valence, id=spotify_id)
		db.session.add(track)
		db.session.commit()
	
	return render_template('track_details.jinja2', info=track_features_data, track=track_data)

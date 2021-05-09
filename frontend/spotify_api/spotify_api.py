import json
from flask import Flask, Blueprint, request, redirect, g, session, abort, render_template
from jinja2 import TemplateNotFound
import requests
from urllib.parse import quote
import os
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from models import User, Artist, Track, connect_db, db

# blueprint configuration
spotify_api_bp = Blueprint(
	'spotify_api_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

# these are all for spotify
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
spotify_auth_url = "https://accounts.spotify.com/authorize"
spotify_token_url = "https://accounts.spotify.com/api/token"
spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"

#  server side information
redirect_uri = os.environ.get("REDIRECT_URI")

# specify what permissions you need based on endpoints
scope = "user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private"
state = ""

app.config["SECRET_KEY"] = "one two three four"

# get the models up and running
SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
connect_db(app)
db.create_all()

# the following spotify authentication code was taken and adapted slightly from this repo
# https://github.com/drshrey/spotify-flask-auth-example/blob/master/main.py

auth_query_parameters = {
	"response_type": "code",
	"redirect_uri": redirect_uri,
	"scope": scope,
	"client_id": client_id
}


@spotify_api_bp.route('/connect', methods=['GET'])
def spotify_auth():
	if session.get('access_token'):
		return redirect("/profile")
	else:
		"""app requests authorization ie redirect to spotify login page"""
		url_args = "&".join([f'{key}={val}' for key, val in auth_query_parameters.items()])
		auth_url = f"{spotify_auth_url}/?{url_args}"
		return redirect(auth_url)


@spotify_api_bp.route("/callback")
def callback():
	# requests refresh and access tokens
	auth_token = request.args['code']
	session['code'] = auth_token
	
	auth_options = {
		"grant_type": "authorization_code",
		"code": str(auth_token),
		"redirect_uri": redirect_uri,
		'client_id': client_id,
		'client_secret': client_secret,
	}
	post_req = requests.post(spotify_token_url, data=auth_options)
	
	# token returned to app
	resp_data = json.loads(post_req.text)
	access_token = resp_data["access_token"]
	session['access_token'] = access_token
	
	return redirect('/profile')


@spotify_api_bp.route('/profile', methods=['GET'])
def profile():
	access_token = session['access_token']
	auth_header = {"Authorization": f"Bearer {access_token}"}
	
	# profile data
	user_profile_endpoint = f"{spotify_api_url}/me"
	profile_resp = requests.get(user_profile_endpoint, headers=auth_header)
	profile_data = json.loads(profile_resp.text)
	print("ewkudhweluhflweuhf", profile_data)
	spotify_id = profile_data['id']
	
	# user top artists
	user_top_artist_endpoint = f"{spotify_api_url}/me/top/artists?limit=5"
	top_artist_resp = requests.get(user_top_artist_endpoint, headers=auth_header)
	top_artist_data = json.loads(top_artist_resp.text)
	
	# user top tracks
	user_top_tracks_endpoint = f"{spotify_api_url}/me/top/tracks?limit=25"
	top_tracks_resp = requests.get(user_top_tracks_endpoint, headers=auth_header)
	top_tracks_data = json.loads(top_tracks_resp.text)
	
	session['curr_user'] = spotify_id
	if not User.query.filter(User.spotify_id == spotify_id).first():
		user = User(spotify_id=spotify_id)

		db.session.add(user)
		db.session.commit()
	return render_template("profile.jinja2", profile=profile_data, artists=top_artist_data, tracks=top_tracks_data)


@spotify_api_bp.route("/artist/<artist_id>", methods=["GET"])
def artist_details(artist_id):
	# access token to access api
	access_token = session['access_token']
	auth_header = {"Authorization": f"Bearer {access_token}"}
	
	# artist
	artist_endpoint = f"{spotify_api_url}/artists/{artist_id}"
	artist_resp = requests.get(artist_endpoint, headers=auth_header)
	artist_data = json.loads(artist_resp.text)
	
	# artist top tracks
	artist_top_tracks_endpoint = f"{spotify_api_url}/artists/{artist_id}/top-tracks?market=US"
	artist_top_tracks_resp = requests.get(artist_top_tracks_endpoint, headers=auth_header)
	artist_top_tracks_data = json.loads(artist_top_tracks_resp.text)
	
	# artists related artist
	artist_related_artist_endpoint = f"{spotify_api_url}/artists/{artist_id}/related-artists"
	artist_related_artist_resp = requests.get(artist_related_artist_endpoint, headers=auth_header)
	artist_related_artist_data = json.loads(artist_related_artist_resp.text)
	
	name = artist_data['name']
	popularity = artist_data['popularity']
	if not artist_data['images']:
		image = '../../static/img/venus.png'
	else:
		image = artist_data['images'][0]['url']
	spotify_id = artist_data['id']
	
	if not Artist.query.get(spotify_id):
		artist = Artist(name=name, popularity=popularity, image=image, id=spotify_id)
		db.session.add(artist)
		db.session.commit()
	elif Artist.query.filter(Artist.popularity == popularity).first():
		pass
	else:
		Artist.query.filter_by(id=spotify_id).update(dict(popularity=popularity, image=image))
		db.session.commit()
	
	return render_template('artist_details.jinja2', artist=artist_data, image=image, top_tracks=artist_top_tracks_data,
	                       related_artist=artist_related_artist_data)


@spotify_api_bp.route("/track/<track_id>", methods=["GET"])
def track_details(track_id):
	if Track.query.get(track_id):
		track = Track.query.get(track_id)
		artist = Artist.query.get(track.artist_id)
		
		return render_template('track_details.jinja2', track=track, artist=artist)
	
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
	
	print(dance)
	
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
	
	if track_data['album']['images'][0]['url']:
		image = track_data['album']['images'][0]['url']
	else:
		image = '/static/placeholder.png'
	
	if Artist.query.get(artist_id) and not Track.query.get(track_id):
		track = Track(title=title, artist_id=artist_id, popularity=popularity, energy=energy, dance=dance,
		              acoustic=acoustic, speech=speech, valence=valence, id=track_id, image=image)
		artist = Artist.query.get(artist_id)
		
		db.session.add(track)
		db.session.commit()
	else:
		name = track_data['artists'][0]['name']
		spotify_id = track_data['artists'][0]['id']
		
		artist = Artist(name=name, id=spotify_id)
		db.session.add(artist)
		db.session.commit()
		
		track = Track(title=title, artist_id=artist_id, popularity=popularity, energy=energy, dance=dance,
		              acoustic=acoustic, speech=speech, valence=valence, id=track_id, image=image)
		
		db.session.add(track)
		db.session.commit()
	
	return render_template('track_details.jinja2', track=track, artist=artist)


@spotify_api_bp.route('/search', methods=['GET'])
def show_search_page():
	return render_template('search_page.jinja2')


@spotify_api_bp.route('/search', methods=['POST'])
def search_spotify_api():
	if not session.get('access_token'):
		return redirect("/connect")
	else:
		search = request.form.get('search')

		access_token = session['access_token']
		auth_header = {"Authorization": f"Bearer {access_token}"}

		# search endpoint
		search_endpoint = f"{spotify_api_url}/search?q={search}&type=track,artist"
		search_resp = requests.get(search_endpoint, headers=auth_header)
		search_data = json.loads(search_resp.text)

		return render_template('search_results.jinja2', search=search_data)
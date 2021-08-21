import json
from flask import Flask, Blueprint, request, redirect, g, session, abort, render_template
from jinja2 import TemplateNotFound
import requests
from urllib.parse import quote
import os
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from models import User, Artist, Track, connect_db, db
from .services.data_parsing import make_get_request
from ..static.services.constants import client_id, client_secret, spotify_auth_url, redirect_uri, spotify_api_url, \
	spotify_token_url, scope, state, danceability, energy, valence, popularity, speechiness, acousticness

default = 0.0

# blueprint configuration
spotify_api_bp = Blueprint(
	'spotify_api_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

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
	if not session.get('access_token'):
		return redirect("/connect")
	else:
		# profile data
		profile_data = make_get_request(f"{spotify_api_url}/me", session)
		spotify_id = profile_data['id']
		
		# user top artists
		top_artist_data = make_get_request(f"{spotify_api_url}/me/top/artists?limit=5", session)
		
		# user top tracks
		top_tracks_data = make_get_request(f"{spotify_api_url}/me/top/tracks?limit=25", session)
		
		session['curr_user'] = spotify_id
		if not User.query.filter(User.spotify_id == spotify_id).first():
			user = User(spotify_id=spotify_id)
			
			db.session.add(user)
			db.session.commit()
		return render_template("profile.jinja2", profile=profile_data, artists=top_artist_data, tracks=top_tracks_data)


@spotify_api_bp.route("/artist/<artist_id>", methods=["GET"])
def artist_details(artist_id):
	if not session.get('access_token'):
		return redirect("/connect")
	elif Artist.query.get(artist_id):
		artist_data = Artist.query.get(artist_id)
		# artist top tracks
		artist_top_tracks_data = make_get_request(f"{spotify_api_url}/artists/{artist_id}/top-tracks?market=US", session)
		
		# artists related artist
		artist_related_artist_data = make_get_request(f"{spotify_api_url}/artists/{artist_id}/related-artists", session)
		return render_template('artist_details.jinja2', artist=artist_data, image=artist_data.image,
		                       top_tracks=artist_top_tracks_data,
		                       related_artist=artist_related_artist_data)
	else:
		# artist
		artist_data = make_get_request(f"{spotify_api_url}/artists/{artist_id}", session)
		
		# artist top tracks
		artist_top_tracks_data = make_get_request(f"{spotify_api_url}/artists/{artist_id}/top-tracks?market=US", session)
		
		# artists related artist
		artist_related_artist_data = make_get_request(f"{spotify_api_url}/artists/{artist_id}/related-artists", session)
		
		name = artist_data['name']
		
		if not artist_data['images']:
			image = '../../static/img/venus.png'
		else:
			image = artist_data['images'][0]['url']
		
		spotify_id = artist_data['id']
		
		if not Artist.query.get(artist_id):
			print("if NOT IN DATA BASE")
			artist = Artist(name=name, popularity=artist_data[popularity], image=image, id=spotify_id)
			db.session.add(artist)
			db.session.commit()
		elif Artist.query.filter(Artist.popularity == popularity).first():
			pass
		else:
			Artist.query.filter_by(id=spotify_id).update(dict(popularity=artist_data[popularity], image=image))
			db.session.commit()
		
		return render_template('artist_details.jinja2', artist=artist_data, image=image, top_tracks=artist_top_tracks_data,
		                       related_artist=artist_related_artist_data)


@spotify_api_bp.route("/track/<track_id>", methods=["GET"])
def track_details(track_id):
	if not session.get('access_token'):
		return redirect("/connect")
	elif Track.query.get(track_id):
		track = Track.query.get(track_id)
		artist = Artist.query.get(track.artist_id)
		
		return render_template('track_details.jinja2', track=track, artist=artist)
	else:
		# track
		track_data = make_get_request(f"{spotify_api_url}/tracks/{track_id}", session)
		
		# track features like popularity and valence
		track_features_data = make_get_request(f"{spotify_api_url}/audio-features/{track_id}", session)
		
		title = track_data['name']
		artist_id = track_data['artists'][0]['id']
		
		if track_data['album']['images'][0]['url']:
			image = track_data['album']['images'][0]['url']
		else:
			image = '/static/placeholder.png'
		
		if Artist.query.get(artist_id) and not Track.query.get(track_id):
			track = Track(title=title, artist_id=artist_id, popularity=track_data[popularity],
			              energy=track_features_data.get(energy, default),
			              dance=track_features_data.get(danceability, default),
			              acoustic=track_features_data.get(acousticness, default),
			              speech=track_features_data.get(speechiness, default),
			              valence=track_features_data.get(valence, default), id=track_id, image=image)
			artist = Artist.query.get(artist_id)
			
			db.session.add(track)
			db.session.commit()
		else:
			name = track_data['artists'][0]['name']
			spotify_id = track_data['artists'][0]['id']
			
			artist = Artist(name=name, id=spotify_id)
			db.session.add(artist)
			db.session.commit()
		
		track = Track(title=title, artist_id=artist_id, popularity=track_data[popularity],
		              energy=track_features_data.get(energy, default),
		              dance=track_features_data.get(danceability, default),
		              acoustic=track_features_data.get(acousticness, default),
		              speech=track_features_data.get(speechiness, default),
		              valence=track_features_data.get(valence, default), id=track_id, image=image)
		
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
		
		# search endpoint
		search_data = make_get_request(f"{spotify_api_url}/search?q={search}&type=track,artist", session)
		
		return render_template('search_results.jinja2', search=search_data)

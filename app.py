import json
from flask import Flask, request, redirect, g, render_template, session
import requests
from urllib.parse import quote
import os
from models import db, connect_db, User, Artist, Track, Genre, Evaluation

app = Flask(__name__)

# these are all for spotify
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
spotify_auth_url = "https://accounts.spotify.com/authorize"
spotify_token_url = "https://accounts.spotify.com/api/token"
spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"

#  server side information
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
redirect_uri = os.environ.get("REDIRECT_URI")
# specify what permissions you need based on endpoints
scope = "user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private"
state = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

app.config["SECRET_KEY"] = "secrets secrets are no fun"

# get the models up and running
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///spotify_evaluation'
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


@app.route("/")
def homepage():
	return render_template('connect.html')


@app.route("/connect")
def spotify_auth():
	# app requests authorization ie redirect to spotify login page
	url_args = "&".join([f'{key}={quote(val)}' for key, val in auth_query_parameters.items()])
	auth_url = f"{spotify_auth_url}/?{url_args}"
	return redirect(auth_url)


@app.route("/callback")
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
	
	refresh_token = resp_data["refresh_token"]
	token_type = resp_data["token_type"]
	expires_in = resp_data["expires_in"]
	
	return redirect('/profile')


@app.route('/profile')
def show_user_info():
	# access token to access api
	if not session.get('access_token'):
		return redirect("/connect")
	else:
		access_token = session['access_token']
		auth_header = {"Authorization": f"Bearer {access_token}"}
		
		# profile data
		user_profile_endpoint = f"{spotify_api_url}/me"
		profile_resp = requests.get(user_profile_endpoint, headers=auth_header)
		profile_data = json.loads(profile_resp.text)
		
		spotify_id = profile_data['id']
		
		# user top artists
		user_top_artist_endpoint = f"{spotify_api_url}/me/top/artists?limit=5"
		top_artist_resp = requests.get(user_top_artist_endpoint, headers=auth_header)
		top_artist_data = json.loads(top_artist_resp.text)
		
		# user top tracks
		user_top_tracks_endpoint = f"{spotify_api_url}/me/top/tracks?limit=25"
		top_tracks_resp = requests.get(user_top_tracks_endpoint, headers=auth_header)
		top_tracks_data = json.loads(top_tracks_resp.text)
		
		if not User.query.filter(User.spotify_id == spotify_id).first():
			user = User(spotify_id=spotify_id)
			db.session.add(user)
			db.session.commit()
		
		return render_template("user_info.html", profile=profile_data, artists=top_artist_data, tracks=top_tracks_data)


# user playlist data
# playlist_endpoint = f"{profile_data['href']}/playlists"
# playlists_resp = requests.get(playlist_endpoint, headers=auth_header)
# playlist_data = json.loads(playlists_resp.text)


@app.route("/artist/<artist_id>")
def show_artist_data(artist_id):
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
	image = artist_data['images'][0]['url']
	spotify_id = artist_data['id']
	
	if not Artist.query.filter(spotify_id == spotify_id).first():
		artist = Artist(name=name, popularity=popularity, image=image, spotify_id=spotify_id)
		db.session.add(artist)
		db.session.commit()
	
	return render_template('artists_details.html', artist=artist_data, top_tracks=artist_top_tracks_data,
	                       related_artist=artist_related_artist_data)


@app.route("/track/<track_id>", methods=["GET"])
def show_track_data(track_id):
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
	
	title = track_data['name']
	artist_id = track_data['artists'][0]['id']
	popularity = track_data['popularity']
	energy = track_features_data['energy']
	dance = track_features_data['danceability']
	acoustic = track_features_data['acousticness']
	speech = track_features_data['speechiness']
	valence = track_features_data['valence']
	spotify_id = track_features_data['id']
	
	# if Artist.query.filter(Artist.spotify_id == artist_id).first():
		# track = Track(title=title, artist_id=artist_id, popularity=popularity, energy=energy, dance=dance,
		#               acoustic=acoustic, speech=speech, valence=valence, spotify_id=spotify_id)
		# db.session.add(track)
		# db.session.add()
		# db.session.commit()
	# else:
	# 	name = track_data['artists'][0]['name']
	# 	spotify_id = track_data['artists'][0]['id']
		
		# artist = Artist(name=name, spotify_id=spotify_id)
		# db.session.add(artist)
		# db.session.commit()
		#
		# track = Track(title=title, artist_id=artist_id, popularity=popularity, energy=energy, dance=dance,
		#               acoustic=acoustic, speech=speech, valence=valence, spotify_id=spotify_id)
		# db.session.add(track)
		# db.session.commit()
	
	return render_template('track_analysis.html', info=track_features_data, track=track_data)


@app.route('/search', methods=['GET'])
def show_search_page():
	return render_template('search_page.html')


@app.route('/search', methods=['POST'])
def search_spotify_api():
	search = request.form.get('search')
	
	access_token = session['access_token']
	auth_header = {"Authorization": f"Bearer {access_token}"}
	
	# search endpoint
	search_endpoint = f"{spotify_api_url}/search?q={search}&type=track,artist"
	search_resp = requests.get(search_endpoint, headers=auth_header)
	search_data = json.loads(search_resp.text)
	
	return render_template('search_result.html', search=search_data)


# @app.route("/logout", methods=["GET", "POST"])
# def logout():
# 	return redirect('/')


@app.route("/about")
def about_page():
	# about page
	return render_template("about.html")

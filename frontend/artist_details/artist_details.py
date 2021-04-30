from flask import render_template, Blueprint, session
from flask import current_app as app
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from models import Artist, connect_db, db

# blueprint configuration
artist_details_bp = Blueprint(
	'artist_details_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"

@artist_details_bp.route("/artist/<artist_id>", methods=["GET"])
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

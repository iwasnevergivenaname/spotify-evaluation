from flask import render_template, Blueprint, session, redirect
from flask import current_app as app
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from models import User, connect_db, db

# blueprint configuration
profile_bp = Blueprint(
	'profile_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

# get the models up and running
SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
connect_db(app)
db.create_all()

#  spotify
spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"


@profile_bp.route('/profile', methods=['GET'])
def profile():
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
		
		session['curr_user'] = spotify_id
		if not User.query.filter(User.spotify_id == spotify_id).first():
			user = User(spotify_id=spotify_id)

			db.session.add(user)
			db.session.commit()

		return render_template("profile.jinja2", profile=profile_data, artists=top_artist_data, tracks=top_tracks_data)

import json
from flask import Flask, Blueprint, request, redirect, g, session, abort
from jinja2 import TemplateNotFound
import requests
from urllib.parse import quote
import os
from flask import current_app as app

# blueprint configuration
spotify_auth_bp = Blueprint(
	'spotify_auth_bp', __name__,
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
# SHOW_DIALOG_bool = True
# SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

app.config["SECRET_KEY"] = "traveling swallowing dramamine"

# the following spotify authentication code was taken and adapted slightly from this repo
# https://github.com/drshrey/spotify-flask-auth-example/blob/master/main.py

auth_query_parameters = {
	"response_type": "code",
	"redirect_uri": redirect_uri,
	"scope": scope,
	"client_id": client_id
}


@spotify_auth_bp.route('/connect', methods=['GET'])
def spotify_auth():
	"""app requests authorization ie redirect to spotify login page"""
	url_args = "&".join([f'{key}={val}' for key, val in auth_query_parameters.items()])
	auth_url = f"{spotify_auth_url}/?{url_args}"
	return redirect(auth_url)


@spotify_auth_bp.route("/callback")
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
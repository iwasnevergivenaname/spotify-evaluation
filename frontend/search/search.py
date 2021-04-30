from flask import render_template, Blueprint, session, request, redirect
from flask import current_app as app
import requests
import json

# blueprint configuration
search_bp = Blueprint(
	'search_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"


@search_bp.route('/search', methods=['GET'])
def show_search_page():
	return render_template('search_page.jinja2')


@search_bp.route('/search', methods=['POST'])
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

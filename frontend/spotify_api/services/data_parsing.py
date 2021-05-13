import requests
import json


def make_get_request(url, options):
	session = options['session']
	access_token = session['access_token']
	auth_header = {"Authorization": f"Bearer {access_token}"}
	spotify_resp = requests.get(api_endpoint, headers=auth_header)
	return json.loads(spotify_resp.text)
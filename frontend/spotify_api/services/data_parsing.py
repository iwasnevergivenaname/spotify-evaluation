from flask import session
import requests
import json


def make_get_request(url, options):
	# session = options['session']
	access_token = options['access_token']
	auth_header = {"Authorization": f"Bearer {access_token}"}
	spotify_resp = requests.get(url, headers=auth_header)
	return json.loads(spotify_resp.text)
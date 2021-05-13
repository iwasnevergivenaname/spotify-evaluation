import requests
import json


def spotify_request(api_endpoint, auth_header):
	spotify_resp = requests.get(api_endpoint, headers=auth_header)
	return json.loads(spotify_resp.text)


def make_get_request(url, options):
	session = options['session']
	access_token = session['access_token']
	auth_header = {"Authorization": f"Bearer {access_token}"}
	spotify_resp = requests.get(api_endpoint, headers=auth_header)
	return json.loads(spotify_resp.text)

# creating an extra function that would take and access token, an api path and an optional
# body and will make a request to spotify - so that you don't have to construct the headers,
# parse json response and do similar things manually every time.

import requests


def spotify_request(api_endpoint, auth_header):
	spotify_resp = requests.get(api_endpoint, headers=auth_header)
	return json.loads(spotify_resp.text)
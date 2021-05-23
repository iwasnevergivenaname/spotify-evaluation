import os
# from collections import defaultdict

# these are all for spotify
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
spotify_auth_url = "https://accounts.spotify.com/authorize"
spotify_token_url = "https://accounts.spotify.com/api/token"
spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"

#  server side information
redirect_uri = 'https://spotify-evaluation.herokuapp.com/callback'
# redirect_uri = os.environ.get("REDIRECT_URI")

# specify what permissions you need based on endpoints
scope = "user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private"
state = ""

# consts = defaultdict(str)
energy = 'energy'
danceability = 'danceability'
acousticness = 'acousticness'
speechiness = 'speechiness'
valence = 'valence'
popularity = 'popularity'
dance = 'danceability'
acoustic = 'acousticness'
speech = 'speechiness'

default = 0.00

from wsgi import app
from flask import session
from unittest import TestCase

app.config['TESTING'] = True

spotify_api_base = "https://api.spotify.com"
API_VERSION = "v1"
spotify_api_url = f"{spotify_api_base}/{API_VERSION}"


class SpotifyAppViewsTestCase(TestCase):
	"""testing app without spotify api"""
	
	def test_home_page(self):
		with app.test_client() as client:
			resp = client.get('/')
			html = resp.get_data(as_text=True)
			
			self.assertEqual(resp.status_code, 200)
			self.assertIn('<h1>judgmental spotify</h1>', html)
			
	def test_auth_redirect(self):
		with app.test_client() as client:
			resp = client.get('/connect')
			
			self.assertEqual(resp.status_code, 302)
			self.assertIn("https://accounts.spotify.com/", resp.location)
			
	def test_about_page(self):
		with app.test_client() as client:
			resp = client.get('/about')
			html = resp.get_data(as_text=True)
			
			self.assertEqual(resp.status_code, 200)
			self.assertIn('<b>how this app uses your data:</b>', html)
	
	def test_search_page(self):
		with app.test_client() as client:
			resp = client.get('/search')
			html = resp.get_data(as_text=True)
			
			self.assertEqual(resp.status_code, 200)
			self.assertIn('<input class="search-bar" id="search" name="search" type="text" placeholder="search">', html)
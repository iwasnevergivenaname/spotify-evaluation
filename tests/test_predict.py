"""python3 -m unittest tests/test_predict.py """

from wsgi import app
import json
from flask import session
from unittest import TestCase
from models import db, connect_db, User

app.config['TESTING'] = True


class ModelPredictionTestCase(TestCase):
	"""testing connection between my frontend/spotify database and my machine learning model"""
	SQLALCHEMY_DATABASE_URI = "postgresql://spotify_evaluation"
	TESTING = True
	
	def test_model_received_data(self):
		with app.test_client() as client:
			
			payload = json.dumps({'title': 'Backseat (feat. Carly Rae Jepsen)', 'acousticness': '0.247',
			                         'danceability': '0.626', 'energy': '0.607', 'speechiness': '0.0409', 'valence': '0.339',
			                         'popularity': '49', 'track_id': '4HjtHraeKy5wA4DA9o92HZ', 'user_id': 'user1'})
			req = client.post('/predict', json=payload)
			# html = resp.get_data(as_text=True)
			
			self.assertEqual(req.status_code, 200)

from flask import redirect, Blueprint, session, request, jsonify
from flask import current_app as app
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from models import Track, Artist, connect_db, db

# blueprint configuration
predict_bp = Blueprint(
	'predict_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

prediction_model_endpoint = 'http://127.0.0.1:8000/predict'


# @train_bp.route('/predict', methods=["GET"])
# def evaluate():
# 	model = requests.get(model_api)
# 	print("🍄", model)
# 	return '<h1>training model</h1>'


@predict_bp.route('/predict', methods=["GET", 'POST'])
def predict():
	# request.form
	track = {'title': request.form.get("title"), 'acousticness': request.form.get("acousticness"),
	         'danceability': request.form.get("danceability"), 'energy': request.form.get("energy"),
	         'speechiness': request.form.get("speechiness"), 'valence': request.form.get("valence"),
	         'popularity': request.form.get("popularity")}
	
	print("🎾", track)
	prediction = requests.post(prediction_model_endpoint, json=track)
	print("🍄", prediction)
	
	return '<h1>training model</h1>'
	# return jsonify(track)
	


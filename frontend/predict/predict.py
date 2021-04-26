from flask import redirect, Blueprint, session, request
from flask import current_app as app
import requests
from flask_sqlalchemy import SQLAlchemy
from models import User, Track, Artist, Genre, Evaluation, connect_db, db

# blueprint configuration
predict_bp = Blueprint(
	'predict_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

prediction_model_endpoint = 'http://127.0.0.1:8000/predict'


@predict_bp.route('/predict/<track_id>', methods=['GET', 'POST'])
def predict(track_id):
	track_id = track_id
	user_id = session['curr_user']
	track = {'title': request.form.get("title"), 'acousticness': request.form.get("acoustic"),
	         'danceability': request.form.get("dance"), 'energy': request.form.get("energy"),
	         'speechiness': request.form.get("speech"), 'valence': request.form.get("valence"),
	         'popularity': request.form.get("popularity"), 'track_id': track_id, 'user_id': user_id}
	
	print("🍄", track)
	
	prediction = requests.post(prediction_model_endpoint, json=track)
	if prediction.status_code == 200:
		return redirect(f'/evaluation/{track_id}')
	return redirect("/error")
	
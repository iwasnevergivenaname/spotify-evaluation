from flask import Blueprint, session, request, render_template, redirect
from flask import current_app as app
import requests
from flask_sqlalchemy import SQLAlchemy
from frontend.prediction.services.alignment import alignment
from models import Track, Evaluation, connect_db, db
import os
from ..static.services.constants import danceability, energy, valence, popularity, speechiness, acousticness, acoustic, \
	speech, dance

# blueprint configuration
prediction_bp = Blueprint(
	'prediction_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

prediction_model_endpoint = os.environ.get("PREDICTION_MODEL_ENDPOINT")


@prediction_bp.route('/predict/<track_id>', methods=['GET', 'POST'])
def predict(track_id):
	track_id = track_id
	user_id = session['curr_user']
	track = {'title': request.form.get("title"), acousticness: request.form.get(acoustic),
	         danceability: request.form.get(dance), energy: request.form.get(energy),
	         speechiness: request.form.get(speech), valence: request.form.get(valence),
	         popularity: request.form.get(popularity), 'track_id': track_id, 'user_id': user_id}
	
	prediction = requests.post(prediction_model_endpoint, json=track)
	print("🌸🌸")
	print(prediction)
	print("🌸🌸")
	if prediction.status_code == 200:
		return redirect(f'/evaluation/{track_id}')
	return redirect("/error")


@prediction_bp.route('/evaluation', methods=["GET", 'POST'])
def resp():
	data = request.get_json()
	track_id = data['track_id']
	result = data['prediction']
	user_id = data['user_id']
	if Evaluation.query.filter_by(track_id=track_id).first():
		pass
	else:
		new_evaluation = Evaluation(user_id=user_id, result=result, track_id=track_id, message=alignment[result])
		db.session.add(new_evaluation)
		db.session.commit()
	return "done"


@prediction_bp.route('/evaluation/<track_id>', methods=["GET", 'POST'])
def evaluation(track_id):
	current_user = session['curr_user']
	track_id = track_id
	track = Track.query.get(track_id)
	title = track.title
	user_evaluation = Evaluation.query.filter_by(track_id=track_id, user_id=current_user).first()
	return render_template('evaluation.jinja2', alignment=user_evaluation, title=title)


@prediction_bp.route('/evaluation/<track_id>/delete', methods=["GET", 'POST'])
def delete_saved_evaluation(track_id):
	current_user = session['curr_user']
	track_id = track_id
	if Evaluation.query.filter_by(track_id=track_id, user_id=current_user).first():
		eval = Evaluation.query.filter_by(track_id=track_id, user_id=current_user).first()
		db.session.delete(eval)
		db.session.commit()
	return redirect(f'/saved/{current_user}')


@prediction_bp.route('/saved/<user_id>', methods=["GET"])
def evaluations(user_id):
	user_id = user_id
	saved = Evaluation.query.filter_by(user_id=user_id)
	return render_template('saved_evaluations.jinja2', saved=saved)

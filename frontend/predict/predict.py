from flask import redirect, Blueprint, session, request, jsonify, render_template
from flask import current_app as app
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from models import Track, Artist, Genre, connect_db, db

# blueprint configuration
predict_bp = Blueprint(
	'predict_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

prediction_model_endpoint = 'http://127.0.0.1:8000/predict'


@predict_bp.route('/predict', methods=['GET', 'POST'])
def predict():
	# request.form
	track = {'title': request.form.get("title"), 'acousticness': request.form.get("acousticness"),
	         'danceability': request.form.get("danceability"), 'energy': request.form.get("energy"),
	         'speechiness': request.form.get("speechiness"), 'valence': request.form.get("valence"),
	         'popularity': request.form.get("popularity")}
	
	print("🎾", track)
	prediction = requests.post(prediction_model_endpoint, json=track)
	print("🍄", prediction)
	# if prediction.status_code == 200:
		# if Genre.query.filter:
		# 	data = session.get('genre')
		# 	print("🦋", data)
		# 	return render_template('predict.jinja2', genre=data)
	return render_template('predict.jinja2')
	

# @predict_bp.route('/evaluation', methods=["GET", 'POST'])
# def evaluation():
# 	req_data = request.get_data()
# 	data = req_data.decode("utf-8")
# 	print("✦", data)
# 	print(judgement(data))
# 	return render_template('predict.jinja2', genre=data)
#
#
# def judgement(genre):
# 	t1 = ['0', '9', 'i', 'q', 'z']
# 	t2 = ['', '1', 'a', 'j', 'r']
# 	t3 = ['2', 'b', 'k', 's', '!']
# 	t4 = ['3', 'c', 'l', 't', '%']
# 	t5 = ['4', 'd', 'm', 'u', '&']
# 	t6 = ['5', 'e', 'n', 'v']
# 	t7 = ['6', 'f', 'o', 'w']
# 	t8 = ['7', 'g', 'o', 'x']
# 	t9 = ['8', 'h', 'p', 'y']
# 	matrix = [t1, t2, t3, t4, t5, t6, t7, t8, t9]
# 	alignment = ['lawful good', 'lawful neutral', 'lawful evil', 'neutral good', 'true neutral', 'neutral evil',
# 	             'chaotic good', 'chaotic neutral', 'chaotic evil']
# 	count = 0
# 	for t in matrix:
# 		count += 1
# 		for i in t:
# 			if genre[0] == i:
# 				return f"{genre} in t{count} matches {i} making you {alignment[count-1]}"
# 		# 	for i in t2:
# 		# if genre[0] == i:
# 		# 	return f"{genre} in t1 matches {i}"
# 	# if genre == "pop":
# 	# 	return "dlfkgbdlkjfbgdkjb"
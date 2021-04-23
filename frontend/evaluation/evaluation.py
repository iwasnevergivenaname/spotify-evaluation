from flask import redirect, Blueprint, session, request, jsonify, render_template
from flask import current_app as app
from models import Track, Artist, Evaluation, connect_db, db
from flask_sqlalchemy import SQLAlchemy
import requests
import json


# blueprint configuration
evaluation_bp = Blueprint(
	'evaluation_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@evaluation_bp.route('/evaluation', methods=["GET", 'POST'])
def resp():
	data = request.get_json()
	track_id = data['track_id']
	result = data['prediction']
	user_id = data['user_id']
	if Evaluation.query.filter_by(track_id=track_id).first():
		pass
	else:
		new_evaluation = Evaluation(user_id=user_id, result=result, track_id=track_id)
		db.session.add(new_evaluation)
		db.session.commit()
	return "done"
	

@evaluation_bp.route('/evaluation/<track_id>', methods=["GET", 'POST'])
def evaluation(track_id):
	track_id = track_id
	alignment = Evaluation.query.filter_by(track_id=track_id).first()
	return render_template('predict.jinja2', alignment=alignment)


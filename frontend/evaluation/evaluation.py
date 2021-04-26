from flask import Blueprint, session, request, render_template, redirect
from flask import current_app as app
from models import Evaluation, Track, connect_db, db
from flask_sqlalchemy import SQLAlchemy

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
	current_user = session['curr_user']
	track_id = track_id
	track = Track.query.get(track_id)
	title = track.title
	evaluation = Evaluation.query.filter_by(track_id=track_id, user_id=current_user).first()
	return render_template('evaluation.jinja2', alignment=evaluation, title=title)


@evaluation_bp.route('/evaluation/<track_id>/delete', methods=["GET", 'POST'])
def delete_saved_evaluation(track_id):
	current_user = session['curr_user']
	track_id = track_id
	if Evaluation.query.filter_by(track_id=track_id, user_id=current_user).first():
		eval = Evaluation.query.filter_by(track_id=track_id, user_id=current_user).first()
		db.session.delete(eval)
		db.session.commit()
	return redirect(f'/saved/{current_user}')
	
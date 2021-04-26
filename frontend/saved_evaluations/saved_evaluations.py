from flask import Blueprint, session, render_template
from flask import current_app as app
from models import Evaluation, connect_db, db
from flask_sqlalchemy import SQLAlchemy

# blueprint configuration
saved_evaluations_bp = Blueprint(
	'saved_evaluations_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@saved_evaluations_bp.route('/saved/<user_id>', methods=["GET"])
def evaluations(user_id):
	user_id = user_id
	saved = Evaluation.query.filter_by(user_id=user_id)
	return render_template('saved_evaluations.jinja2', saved=saved)
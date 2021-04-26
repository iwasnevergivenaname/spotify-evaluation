from flask import render_template, Blueprint
from flask import current_app as app

# blueprint configuration
home_bp = Blueprint(
	'home_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@home_bp.route('/', methods=['GET'])
def home():
	"""homepage"""
	return render_template('home.jinja2')

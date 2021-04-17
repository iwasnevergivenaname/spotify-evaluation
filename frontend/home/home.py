from flask import render_template, Blueprint
from flask import current_app as app
# from frontend.api import fetch_products

# Blueprint Configuration
home_bp = Blueprint(
	'home_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@home_bp.route('/', methods=['GET'])
def home():
	"""homepage"""
	# products = fetch_products(app)
	return render_template(
		'home.jinja2',
		title='Flask Blueprint Demo',
		subtitle='Demonstration of Flask blueprints in action.',
		template='home-template',
		# products=products
	)

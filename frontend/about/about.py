from flask import render_template, Blueprint
from flask import current_app as app

# blueprint configuration
about_bp = Blueprint(
	'about_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@about_bp.route("/about")
def about():
	# about page
	return render_template("about.jinja2")
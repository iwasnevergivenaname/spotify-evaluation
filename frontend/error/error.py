from flask import redirect, Blueprint, render_template
from flask import current_app as app

# blueprint configuration
error_bp = Blueprint(
	'error_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@error_bp.route("/error")
def error():
	return render_template("error.jinja2")

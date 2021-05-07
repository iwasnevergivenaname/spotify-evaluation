from flask import render_template, Blueprint
from flask import current_app as app

# blueprint configuration
static_pages_bp = Blueprint(
	'static_pages_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@static_pages_bp.route('/', methods=['GET'])
def home():
	"""homepage"""
	return render_template('home.jinja2')


@static_pages_bp.route("/about")
def about():
	# about page
	return render_template("about.jinja2")


@static_pages_bp.route('/logout', methods=["GET"])
def logout():
	# print("beep ebeep")
	# session.pop('access_token', None)
	# print('logging out')
	return redirect("/")


@static_pages_bp.route("/beep")
def test():
	return "beep"


@static_pages_bp.route("/error")
def error():
	return render_template("error.jinja2")
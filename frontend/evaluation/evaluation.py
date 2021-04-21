from flask import redirect, Blueprint, session, request, jsonify
from flask import current_app as app
import requests
import json

# blueprint configuration
evaluation_bp = Blueprint(
	'evaluation_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@evaluation_bp.route('/evaluation', methods=["GET", 'POST'])
def evaluation():
	req_data = request.get_data()
	print("🦋", req_data)
	return"<h1>evaluation</h1>"

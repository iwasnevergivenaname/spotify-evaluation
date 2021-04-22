from flask import redirect, Blueprint, session, request, jsonify, render_template
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
	data = req_data.decode("utf-8")
	print("✦", data)
	return render_template('predict.jinja2', genre=data)


# def judgement(genre):
# 	alignment = ['lawful good', 'lawful neutral', 'lawful evil', 'neutral good', 'true neutral', 'neutral evil',
# 	             'chaotic good', 'chaotic neutral', 'chaotic evil']
# 	for i in alignment:
# 		if i == genre:
# 			print("🐳", genre)
#

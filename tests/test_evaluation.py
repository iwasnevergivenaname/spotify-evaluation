"""python3 -m unittest tests/test_evaluation.py """

from wsgi import app
from flask import session
from unittest import TestCase

app.config['TESTING'] = True



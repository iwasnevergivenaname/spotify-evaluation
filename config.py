import os

DIALECT = 'postgresql'
DRIVER = 'psycopg'
USERNAME = 'username'
PASSWORD = 'password'
HOST = '127.0.0.1'
PORT = '5000'
DATABASE = 'spotify_evaluation_dev'
# SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
#                                                                        DATABASE)
DATABASE_URL = 'postgresql://spotify_evaluation_dev'
SQLALCHEMY_DATABASE_URI = 'postgres://canguvfyjkvtbx:58e8c1e670c4619c5e06c363b6d127a53ea7245452eeb20d739a90a0776b1b30@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d25s4qct6bnu2j'

SQLALCHEMY_TRACK_MODIFICATIONS = False

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

#
# class Config(object):
#   DEBUG = False
#   TESTING = False
#   CSRF_ENABLED = True
#   SECRET_KEY = 'this-really-needs-to-be-changed'
#   SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///spotify_evaluation'


# #
# """Class-based Flask app configuration."""
# from os import environ, path
#
# from dotenv import load_dotenv
#
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, ".env"))
#
#
# class Config:
#     """Configuration from environment variables."""
#
#     # SECRET_KEY = environ.get("SECRET_KEY")
#     # FLASK_ENV = environ.get("FLASK_ENV")
#     FLASK_APP = "wsgi.py"
#
#     # Static Assets
#     STATIC_FOLDER = "static"
#     TEMPLATES_FOLDER = "templates"
#     COMPRESSOR_DEBUG = True
#
#     # API
#     CLIENT_ID = environ.get("CLIENT_ID")
#     CLIENT_SECRET = environ.get("CLIENT_SECRET")
#     REDIRECT_URI = environ.get("REDIRECT_URI")

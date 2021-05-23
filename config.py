import os
#
# D = 'postgresql'
# USERNAME = 'username'
# PASSWORD = 'password'
# HOST = '127.0.0.1'
# PORT = '5000'
# DATABASE = 'spotify_evaluation'
# SQLALCHEMY_DATABASE_URI = "postgresql://username:password@127.0.0.1:5000/spotify_evaluation??client_encoding=utf8"
# DATABASE_URL = '://spotify_evaluation'
SQLALCHEMY_DATABASE_URI = 'postgres://dkrwgjkiisnzkc:748626c57cf65eca1e20ee1b3b3c44c5bfd217e59c289ea39ad81042ef85279e@ec2-54-160-96-70.compute-1.amazonaws.com:5432/d49mcq21tdbt13'
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

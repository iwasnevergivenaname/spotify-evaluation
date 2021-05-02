DIALECT = 'postgresql'
DRIVER = 'psycopg'
USERNAME = 'username'
PASSWORD = 'password'
HOST = '127.0.0.1'
PORT = '5000'
DATABASE = 'spotify_evaluation'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)


SQLALCHEMY_TRACK_MODIFICATIONS = False



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
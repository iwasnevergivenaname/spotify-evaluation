from flask import Flask


def create_app():
    """create flask application"""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    with app.app_context():
        # import parts of our application
        from .home import home
        # from .profile import routes
        # from .search import routes
        # from .song_details import routes
        # from .artist_details import routes

        # register blueprints
        app.register_blueprint(home.home_bp)
        # app.register_blueprint(profile.profile_bp)
        # app.register_blueprint(search.search_bp)
        # app.register_blueprint(song_details.song_details_bp)
        # app.register_blueprint(artist_details.artist_details_bp)

        return app
from flask import Flask
from app.config import Config
from app.setup_db import db
from flask_restx import Api
from app.models import Movie, Genre, Director
from app.views.directors.directors import director_ns
from app.views.movies.movies import movie_ns
from app.views.genres.genres import genre_ns


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def register_extensions(application: Flask):
    db.init_app(application)
    api = Api(application)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)


def load_data():
    m1 = Movie(
        title='Test1',
        description='Test1',
        trailer='Test1',
        year=1980,
        rating='Test1',
        genre_id=1,
        director_id=1
    )
    m2 = Movie(
        title='Test2',
        description='Test2',
        trailer='Test2',
        year=1980,
        rating='Test2',
        genre_id=2,
        director_id=2
    )
    g1 = Genre(name='PG13')
    g2 = Genre(name='Adult')
    d1 = Director(name='Christopher')
    d2 = Director(name='James')

    db.create_all()

    with db.session.begin():
        db.session.add_all([m1, m2])
        db.session.add_all([g1, g2])
        db.session.add_all([d1, d2])


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)

    register_extensions(app)
    load_data()

    app.run()




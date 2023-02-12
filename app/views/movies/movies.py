from flask import request
from flask_restx import Resource, Namespace

from app.setup_db import db
from app.models import MovieSchema, Movie

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        if request.args.get(key='director_id') is not None:
            did = request.args.get(key='director_id')
            movies = db.session.query(Movie).filter(Movie.director_id == did).all()
        elif request.args.get(key='genre_id') is not None:
            gid = request.args.get(key='genre_id')
            movies = db.session.query(Movie).filter(Movie.genre_id == gid).all()
        elif request.args.get(key='year') is not None:
            year = request.args.get(key='year')
            movies = db.session.query(Movie).filter(Movie.year == year).all()
        else:
            movies = db.session.query(Movie).all()
        return movies_schema.dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            genre = db.session.query(Movie).filter(Movie.id == mid).one()
            return movie_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, mid: int):
        movie = db.session.query(Movie).get(mid)

        db.session.delete(movie)
        db.session.commit()

        return "", 204


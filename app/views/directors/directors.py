from flask import request
from flask_restx import Resource, Namespace

from app.setup_db import db
from app.models import DirectorSchema, Director

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        all_genres = db.session.query(Director).all()
        return directors_schema.dump(all_genres), 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            genre = db.session.query(Director).filter(Director.id == did).one()
            return director_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404



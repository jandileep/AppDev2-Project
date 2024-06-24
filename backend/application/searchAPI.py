from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from flask import jsonify
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os
theatre_fields = {
    "the_id" : fields.String,
    "the_name" : fields.String,
    "location" : fields.String,
    "place": fields.String,
    "capacity" : fields.String,

}
movie_fields = {
    "movie_id" : fields.String,
    "langauge" : fields.String,
    "movie_name" : fields.String,
    "ratings" : fields.String,
    "timing":fields.String,
    "tags" : fields.String,
    "price" : fields.String,
    "movie_pic":fields.String

}


class placeAPI(Resource):
    @marshal_with(theatre_fields)
    def get(self,place):
        
        theatres = Theatre.query.filter_by(place=place).all()
        return theatres
    
class languageAPI(Resource):
    @marshal_with(movie_fields)
    def get(self,language):
        movies = Movie.query.filter_by( langauge = language).all()
        return movies



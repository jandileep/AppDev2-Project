from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from flask import jsonify
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os

class All_PlaceAPI(Resource):
    def get(self):
        theatres = Theatre.query.all()
        l = []
        for k in theatres:
            l.append(k.place)
        return list(set(l))
    
class All_LanguageAPI(Resource):
    def get(self):
        movies = Movie.query.all()
        l = []
        for k in movies:
            l.append(k.langauge)
        return list(set(l))
    

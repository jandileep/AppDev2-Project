from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os
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
class Theatre_movie_det(Resource):
    @jwt_required()
    @marshal_with(movie_fields)
    def get(self,the_id):
        current_user= get_jwt_identity()
        
        token = request.headers.get('Authorization').split()[1]
        # bearer, token
        decoded_token = decode_token(token)
        if 'admin' or 'user' in  decoded_token['role']:
            # data = request.get_json()
            
            # the_id = data['the_id']
        
            
            theat = TheatreMovie.query.filter_by(the_id = the_id).all()

            l = []
            for mov in theat:
                mov_id = mov.movie_id
                mov_to = Movie.query.filter_by(movie_id=mov_id).first()
                l.append(mov_to)




            return l
        return {'message' : "You are not Authorized to perform this action"}, 400
    @jwt_required()
    def post(self):
        # token = request.headers.get("Authorization").split()[1]
        # decoded_token = decoded_token(token)
        # if "admin" in decoded_token['role']:
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)

        if 'admin' in decoded_token['role']:

            data = request.get_json()
            movie_id = data['movie_id']
            the_id = data['the_id']
        
            movie_theat = TheatreMovie(the_id = the_id, movie_id=movie_id)
            db.session.add(movie_theat)
                
            db.session.commit()
            return {"message" : "Movie added successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform the action"}
            


            


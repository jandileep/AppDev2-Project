from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os
theatre_fields = {
    "the_id" : fields.String,
    "movie_id":fields.String,
    "available_seats" : fields.String,
    "timings":fields.String,
    "price" : fields.Float,
    "capacity":fields.String

}
class Theatre_movie(Resource):
    @jwt_required()
    @marshal_with(theatre_fields)
    def get(self,the_id):
        current_user= get_jwt_identity()
        
        token = request.headers.get('Authorization').split()[1]
        # bearer, token
        decoded_token = decode_token(token)
        if 'admin' in decoded_token['role']:
            # data = request.get_json()
            
            # the_id = data['the_id']
        
            
            theat = TheatreMovie.query.filter_by(the_id = the_id).all()
            # t = Theatre.query.filter_by(the_id=the_id).first()
            # for i in theat:
            #     i['capacity']=t.capacity
            # theat['capacity']= t.capacity
            print(the_id)
            return theat
        if 'user' in decoded_token['role']:
            theat = TheatreMovie.query.filter_by(id = the_id).all()

            print(the_id)
            return theat
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
            print(data)
            movie_id = data['movie_id']
            the_id = data['the_id']
            timings=data['timings']
            price=data['price']
            theatre = Theatre.query.filter_by(the_id=the_id).first()
            
            
       
       
            
       
            
            # available_seats =data['available_seats']
          
            movie_theat = TheatreMovie(the_id = the_id, movie_id=movie_id,timings=timings,price=price,available_seats=theatre.capacity)
            db.session.add(movie_theat)
                
            db.session.commit()
            print(data)
            return {"message" : "Movie added successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform the action"}
            


            


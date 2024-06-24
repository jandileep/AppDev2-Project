from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os

movie_fields = {
"user_id" : fields.String,
    "movie_the_id" : fields.String,
    "seat_number" : fields.String,

}

class BookingAPI(Resource):
    @jwt_required()
    @marshal_with(movie_fields)
    def get(self, movie_the_id):
        current_user= get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        # bearer, token
        decoded_token = decode_token(token)
        if 'admin'or 'user' in  decoded_token['role']:
            
            bookings = Bookings.query.filter_by(movie_the_id = movie_the_id).all()
            return bookings
        return {'message' : "You are not Authorized to perform this action"}, 400
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)

        if 'user' in decoded_token['role']:
            data = request.get_json()
            movie_the_id = data['movie_the_id']
            seat_numbers = data['seat_number']
            theat_movie = TheatreMovie.query.filter_by(id = movie_the_id).first()
            
            
            for seat_number in seat_numbers:
                movie = Bookings(booking_id = str(uuid.uuid4()),user_id = current_user, seat_number=seat_number,movie_the_id=movie_the_id)
                theat_movie.available_seats -= 1
                db.session.add(movie)
           
                
            db.session.commit()
            return {"message" : "Booking done Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
        
    def delete(self, movie_id):
        # return "Hello", 200
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        

        decoded_token = decode_token(token)
       
        if 'admin' in decoded_token['role']:
            movie = Movie.query.filter_by(id = movie_id).first()
    
            db.session.delete(movie)
            db.session.commit()
            return {"message" : "Movie Deleted Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
    


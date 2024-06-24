from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os

movie_fields = {

   "movie_the_id": fields.String,
    "booked_seats":fields.String,
    "theatre_name": fields.String,
    "movie_name": fields.String,
    "movie_pic": fields.String,
    "timings": fields.String,
    "location":fields.String

}

class MyBookingAPI(Resource):
    @jwt_required()
    @marshal_with(movie_fields)
    def get(self):
        current_user= get_jwt_identity()
        
        token = request.headers.get('Authorization').split()[1]
        # bearer, token
        decoded_token = decode_token(token)
        if 'admin'or 'user' in  decoded_token['role']:
            l=[]
            bookings = Bookings.query.filter_by(user_id=current_user).all()
            print(current_user)
            for i in bookings:
                if(i.movie_the_id not in l):
                    l.append(i.movie_the_id)
            m=[]
            for i in l:
                d={}
            
                k=[]
                for j in bookings:
                    if j.movie_the_id==i:
                        k.append(j.seat_number)
                        

                d["movie_the_id"]=i
                d["booked_seats"]=k
                d["no_of_seats"]=len(k)

                the=TheatreMovie.query.filter_by(id=i).first()
                theatre=Theatre.query.filter_by(the_id=the.the_id).first()
                movie=Movie.query.filter_by(movie_id=the.movie_id).first()
                d['theatre_name']=theatre.the_name
                d['movie_name']=movie.movie_name
                d['movie_pic']=movie.movie_pic
                d['timings']=the.timings
                d['location']=theatre.location
              
                m.append(d)
            
            
           

            return m
        return {'message' : "You are not Authorized to perform this action"}, 400
   

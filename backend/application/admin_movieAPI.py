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
    "theatre_name":fields.String,
    "movie_theat_id":fields.String,
    "the_name":fields.String,
    "capacity":fields.String,



    # "ratings" : fields.String,
    "the_id":fields.String,
    "timing":fields.String,
    # "tags" : fields.String,
    "price" : fields.String,
    "movie_pic":fields.String,
    "available_seats" : fields.Integer

}
class Admin_Movie_Theatre(Resource):
    @jwt_required()
    @marshal_with(movie_fields)
    def get(self,the_id,movie_id):
        current_user= get_jwt_identity()
        
        token = request.headers.get('Authorization').split()[1]
        # bearer, token
        decoded_token = decode_token(token)
        if 'admin' or 'user' in  decoded_token['role']:
            # data = request.get_json()
            
            # the_id = data['the_id']
        
            
            theat = TheatreMovie.query.filter_by(movie_id=movie_id,the_id=the_id).all()
       
            final = []
            for x in theat:
                print(x.available_seats)
                d = {}
            
                theID = x.the_id
                a = Theatre.query.filter_by(the_id=theID).first()
                d['the_name']=a.the_name
                d['capacity']=a.capacity
       
           
          
                p = Movie.query.filter_by(movie_id=movie_id).first()
             
               
                d['the_id'] = theID
          
                d["movie_name"]=p.movie_name
                d['timing']=x.timings
                d['movie_pic']=p.movie_pic
                d['langauge']=p.langauge
                d['movie_id']=movie_id
                d['price']=x.price
                d['available_seats'] = x.available_seats  
            
                d['movie_theat_id']=x.id
              

                final.append(d)

         




            return final



           
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
            


            


from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from flask import jsonify
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os

# class Theatre(db.Model):
#     __tablename__ = 'theatre'
#     id = db.Column(db.Integer(), primary_key=True)
#     the_id = db.Column(db.Integer())
#     the_pic = db.Column(db.Text())
#     the_name = db.Column(db.String(50))
#     location = db.Column(db.String())
#     capacity = db.Column(db.String())
#     admin_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
#     the_mov = db.relationship('TheatreMovie', cascade='all, delete')
theatre_fields = {
    "the_id" : fields.String,
    "the_name" : fields.String,
    "location" : fields.String,
    "place": fields.String,
    "capacity" : fields.String,

}

class theatreAPI(Resource):
    @jwt_required()
    @marshal_with(theatre_fields)
    def get(self):
        current_user= get_jwt_identity()
      
        token = request.headers.get('Authorization').split()[1]
        # bearer, token
        decoded_token = decode_token(token)
        if 'admin' in  decoded_token['role']:
        
            
            theat = Theatre.query.filter_by(admin_id = current_user).all()

            return theat
      
        return {'message' : "You are not Authorized to perform this action"}, 400
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)

        if 'admin' in decoded_token['role']:

            data = request.get_json()
            the_name = data['the_name']
            location = data['location']
            capacity = data['capacity']
            place = data["place"]
            print(data)
           
            # folder_path = f'static/shows/{current_user}'
            # theatres = theatres.split(',')
            
            
            # try:
            #     os.makedirs(folder_path, exist_ok=True)
            #     request.files['movie_pic'].save(os.path.join(folder_path, movie_name))
            # except:
            #     return 'Invalid file type', 400
            theatre = Theatre(the_name = the_name, the_id = str(uuid.uuid4()), location=location,capacity=capacity,
                           admin_id = current_user, place=place)
            db.session.add(theatre)
            # for theatreID in theatres:
            #     theatre = Theatre.query.filter_by(theatre_id = theatreID).first()
            #     previous_movie = TheatreMovie.query.filter_by(movie_id = theatre.id).all()
            #     start_time, end_time = timings.split(' - ')
            #     for movie in previous_movie:
            #         show_start_time, show_end_time = movie.timings.split(' - ')

            #         # Check for clash in timings
            #         if start_time <= end_time and end_time >= show_start_time:
            #             return f"Clash in timings with existing show '{movie.movie_name}'", 403
                
            #     mov_the = TheatreMovie(movie_id = movie.id, theatre_id = theatre.id, timings = timings)

            #     theatre.the_mov.append(mov_the)
                
            db.session.commit()
            return {"message" : "Theatre created Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
        
    @jwt_required()
    def put(self,the_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)

        if 'admin' in decoded_token['role']:
            data = request.get_json()
            the_name = data['the_name']

            sql = db.session.query(Theatre).filter(Theatre.the_id == the_id).first()

            if sql is None:
                return jsonify({'message': 'Theatre not found'}), 404

            sql.the_name = the_name
            db.session.commit()
        return "Theatre edited successfully"
    
        
    def delete(self, the_id):
        # return "Hello", 200
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        

        decoded_token = decode_token(token)
       
        if 'admin' in decoded_token['role']:
          
            the_mov = TheatreMovie.query.filter_by(the_id=the_id).all()
            book = Bookings.query.all()
            l = []
            for i in the_mov:
                l.append(i.id)
            for j in book:
                if j.movie_the_id in l:
                    db.session.delete(j)
            db.session.commit()
     
            

            theatre = Theatre.query.filter_by(the_id = the_id).first() 
      
         
            db.session.delete(theatre)

            db.session.commit()
            the_mov = TheatreMovie.query.filter_by(the_id=the_id).all()
            for k in the_mov:
                db.session.delete(k)
            db.session.commit()
            return {"message" : "Theatre Deleted Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
    

from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from flask import jsonify
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

class MovieAPI(Resource):
    @jwt_required()
    @marshal_with(movie_fields)
    def get(self):
        current_user= get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        # bearer, token
        decoded_token = decode_token(token)
        if 'admin'  in  decoded_token['role']:
            
            movies = Movie.query.filter_by(admin_id = current_user).all()
            return movies
        else:
            movies = Movie.query.all()
            
            return movies[::-1]
          
        return {'message' : "You are not Authorized to perform this action"}, 400
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)

        if 'admin' in decoded_token['role']:
            # data = request.get_json()
            # print(data)
          
            
            movie_name = request.form.get('movie_name')
        
            tags = request.form.get('tags')
            price = request.form.get('price')
            rating = request.form.get('rating')
            timing = request.form.get('timing')
            language = request.form.get('language')
            
            file = request.files["movie_pic"]
            print(movie_name)
            print(current_user)
            # return 
            folder_path = f'static/movies/{current_user}'
            import os
            try:
                os.makedirs(folder_path,exist_ok=True)

                request.files['movie_pic'].save(os.path.join(folder_path, file.filename))
                print("File added success")
             
               
            except:
                return "wrong file type", 400
        
            movie = Movie(movie_name = movie_name, movie_id = str(uuid.uuid4()),
                           admin_id = current_user,tags=tags,price=price,timings=timing,langauge=language,movie_pic=f'/{current_user}/{file.filename}',
                          ratings=rating)
            db.session.add(movie)
            
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
            print(movie.movie_name)
            return {"message" : "Movie created and added to respective theatres Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
    @jwt_required()
    def put(self,movie_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)

        if 'admin' in decoded_token['role']:
            data = request.get_json()
            movie_name = data['movie_name']

            sql = db.session.query(Movie).filter(Movie.movie_id == movie_id).first()

            if sql is None:
                return jsonify({'message': 'Movie not found'}), 404

            sql.movie_name = movie_name
            db.session.commit()
        return "Movie edited successfully"    
    def delete(self, movie_id):
        # return "Hello", 200
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        

        decoded_token = decode_token(token)
       
        if 'admin' in decoded_token['role']:
          
            the_mov = TheatreMovie.query.filter_by(movie_id=movie_id).all()
            book = Bookings.query.all()
            l = []
            for i in the_mov:
                l.append(i.id)
            for j in book:
                if j.movie_the_id in l:
                    db.session.delete(j)
            db.session.commit()
     
            

            movie1 = Movie.query.filter_by(movie_id = movie_id).first() 
      
         
            db.session.delete(movie1)

            db.session.commit()
            the_mov = TheatreMovie.query.filter_by(movie_id=movie_id).all()
            for k in the_mov:
                db.session.delete(k)
            db.session.commit()
            return {"message" : "Movie Deleted Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
    


from .database import db

class Users(db.Model):
   __tablename__ = "users"
   id = db.Column(db.Integer, primary_key=True)
#    profile_pic = db.Column(db.Text())
   public_id = db.Column(db.Integer())
   name = db.Column(db.String(50))
   password = db.Column(db.String(50))
   lastseen = db.Column(db.Float())
   email = db.Column(db.String())
   active = db.Column(db.Boolean())
   role = db.Column(db.String())
   bookings = db.relationship('Bookings', cascade='all, delete')
   # language = db.Column(db.String(50))




class Theatre(db.Model):
    __tablename__ = 'theatre'
    id = db.Column(db.Integer(), primary_key=True)
    the_id = db.Column(db.Integer())
    # the_pic = db.Column(db.Text())
    the_name = db.Column(db.String(50))
    place = db.Column(db.String())
    location = db.Column(db.String())
    capacity = db.Column(db.String())
    admin_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    the_mov = db.relationship('TheatreMovie', cascade='all, delete')


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer(), primary_key=True)
    movie_id = db.Column(db.Integer())
    langauge = db.Column(db.String())
    movie_pic = db.Column(db.Text())
    movie_name = db.Column(db.String(50))
    ratings = db.Column(db.Integer())
    timings = db.Column(db.String())
    tags = db.Column(db.String())
    price = db.Column(db.Float())
    admin_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    m_theatres = db.relationship('TheatreMovie', cascade='all, delete')
    

class TheatreMovie(db.Model):
    __tablename__ = "theatre_movie"
    id = db.Column(db.Integer(), primary_key = True)

    movie_id = db.Column(db.Integer(), db.ForeignKey(Movie.id, ondelete='CASCADE'))
    the_id = db.Column(db.Integer(), db.ForeignKey(Theatre.id, ondelete='CASCADE'))
    bookings = db.relationship('Bookings', cascade='all, delete')
    available_seats = db.Column(db.Integer())
    timings=db.Column(db.String())
    price=db.Column(db.String())


class Bookings(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   booking_id=db.Column(db.String())
   user_id = db.Column(db.String(), db.ForeignKey('users.id' , ondelete='CASCADE'))
   seat_number=db.Column(db.Integer())
   movie_the_id= db.Column(db.Integer(), db.ForeignKey('theatre_movie.id', ondelete='CASCADE'))
 

   
# db.create_all()
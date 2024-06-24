import time
from application.workers import celery
from datetime import datetime
from .send_email import send_email
from jinja2 import Template
from flask import current_app as app
from flask_sse import sse
from celery.schedules import crontab
from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
# from weasyprint import HTML
import csv

import uuid
from .models import Users,Theatre, Movie, TheatreMovie, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os
print("crontab ", crontab)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("hello")
    sender.add_periodic_task(10.0, send_reminder.s(), name='add every 10')
    sender.add_periodic_task(20.0, monthly_reminder.s(), name='add every Month')

@celery.task()
def send_reminder():
    now=time.time()
    delta = now-10
    print(delta)
    inactive_users=Users.query.filter(Users.lastseen < delta).all()
    template_file='Reminder/email.html'
    for a in inactive_users:
        with open(template_file) as f:
            temp = Template(f.read())
            msg = temp.render(data=a)

        send_email(a.email, msg, subject="Timely Reminder")
    return len(inactive_users)

def format_report(template_file, data={}, movies={}, theatres={}):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data, movies = movies, theatres = theatres)
    
# def create_pdf_report(data, template_html, movies, theatres):
#     message = format_report(template_html, data = data, movies = movies, theatres = theatres)
#     html = HTML(string = message)
#     file_name = f"EXPORT_files/{str(data.name)}.pdf"
#     print(file_name)
#     html.write_pdf(target = file_name)
def generate_monthly_reminder(user_id):
    
    bookings = Bookings.query.filter_by(user_id=user_id).all()
    # return bookings
    movie_counts = {}
    theatre_counts = {}

    for booking in bookings:
        movie_the_id = booking.movie_the_id
        theatre_movie = TheatreMovie.query.filter_by(id= movie_the_id).first()
        print(theatre_movie, "Hello Janani")
        movie = Movie.query.filter_by(movie_id = theatre_movie.movie_id).first()
        movie_name = movie.movie_name
        movie_counts[movie_name] = movie_counts.get(movie_name, 0) + 1
        theatre = Theatre.query.filter_by(the_id = theatre_movie.the_id).first()
        theatre_counts[theatre.the_name] =  theatre_counts.get(theatre.the_name, 0) + 1



    
   
    return movie_counts,  theatre_counts

@celery.task()
def monthly_reminder():
    us = Users.query.all()
    for user in us:
        if user.role=='user':
            # movies, theatres = generate_monthly_reminder(user.id)
            movies, theatres = generate_monthly_reminder(user.public_id)
            # print(x)
            print(movies, theatres)
            file_path_temp = "templates/template.html"
            f = open(file_path_temp,'r')
            template = Template(f.read())
            msg = template.render(data=user,movies=movies,theatres=theatres)
            send_email(user.email,msg,subject=f"Monthly Engagements {user.name}")





@celery.task()
def export_csv_theatres(the_id):
    print("Hello")
    theatre = Theatre.query.filter_by(the_id = the_id).first()
    theatre_movie = TheatreMovie.query.filter_by(the_id = the_id).all()
    no_of_shows = len(theatre_movie) 
    
    filename = f"{theatre.the_id}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Venue Name', 'Location', 'Capacity', 'No. of Shows'])
        
        writer.writerow([theatre.the_name, theatre.place, theatre.capacity, no_of_shows])
    return filename


@celery.task()
def export_csv_movies(movie_id):
    print("Hello")
    movie = Movie.query.filter_by(movie_id = movie_id).first()
    # theatre_movie = TheatreMovie.query.filter_by(movie_id = movie_id).all()
    # no_of_shows = len(theatre_movie) 
    
    filename = f"{movie.movie_id}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Movie Name', 'Rating', 'Tags', 'Language'])
        
        writer.writerow([movie.movie_name, movie.ratings, movie.tags, movie.langauge])
    return filename




    


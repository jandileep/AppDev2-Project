import os
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from flask_cors import CORS
from application.database import db
from application.tasks import *
from flask_jwt_extended import JWTManager
from application.models import Users
from application.showAPI import MovieAPI
from application import workers

CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
app = None
api = None
celery = None
app = None
api = None
celery = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    print(os.getenv('ENV', "development"))
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      print("pushed config")
    app.app_context().push()
    print("DB Init")
    db.init_app(app)
    print("DB Init complete")
    app.app_context().push()
    app.logger.info("App setup complete")
    # Setup Flask-Security
    
    api = Api(app)
    app.app_context().push()   
    
    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )

    celery.Task = workers.ContextTask
    app.app_context().push()
    print("Create app complete")
    return app, api, celery

app, api, celery = create_app()

# def create_app():
    
#     app = Flask(__name__)
#     if os.getenv("ENV","development") == "production":
#         raise Exception("Currently no production config is setup.")
#     else:
#         print("Starting Local Development")
#         app.config.from_object(LocalDevelopmentConfig)
#     db.init_app(app)
    
    
#     api = Api(app)
#     app.app_context().push()
#     celery = workers.celery
#     celery.conf.update(
#         broker_url = CELERY_BROKER_URL,
#         result_backend = CELERY_RESULT_BACKEND
#     )
#     celery.Task = workers.ContextTask
#     app.app_context().push()
#     return app, api, celery

app, api, celery = create_app()

cors = CORS(app) # Allow cross-origin requests
api = Api(app)

jwt = JWTManager(app)
with app.app_context():
    db.create_all()


from application.userAPI import UserApi
from application.showAPI import MovieAPI
from application.theatreAPI import theatreAPI
from application.theatre_movieAPI import Theatre_movie
from application.theat_mov_detAPI import Theatre_movie_det
from application.movie_theatAPI import Movie_Theatre
from application.MyBookingAPI import MyBookingAPI
from application.bookingsAPI import BookingAPI
from application.admin_movieAPI import Admin_Movie_Theatre
from application.controllers import *
from application.login import *
from application.searchAPI import *
from application.place_langAPI import *
api.add_resource(UserApi,"/api/profile")
api.add_resource(All_LanguageAPI,"/api/all_language")
api.add_resource(All_PlaceAPI,"/api/all_place")
api.add_resource(MovieAPI,"/api/movie","/api/movie/<movie_id>")
api.add_resource(languageAPI,"/api/search_language/<language>")
api.add_resource(placeAPI,"/api/search_place/<place>")
api.add_resource(theatreAPI,"/api/theatre","/api/theatre/<the_id>")
api.add_resource(Theatre_movie,"/api/movie_theatre/<the_id>",'/api/movie_theatre')
api.add_resource(Theatre_movie_det,'/api/theat_mov_det/<the_id>')
api.add_resource(Movie_Theatre,'/api/movie_theatre_user/<movie_id>')
api.add_resource(BookingAPI,"/api/booking", "/api/booking/<movie_the_id>")
api.add_resource(MyBookingAPI,"/api/mybooking")
api.add_resource(Admin_Movie_Theatre,"/api/admin_movie/<the_id>/<movie_id>")


# import time
# from application.workers import celery
# from datetime import datetime
# from flask import current_app as app
# from flask_sse import sse
# from celery.schedules import crontab
# print("crontab ", crontab)


# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     print("hello")
#     sender.add_periodic_task(10.0, hello.s(), name='add every 10')
    

# @celery.task()
# def hello():
#     print("Hello World")
#     return "Task done"

# @celery.task()
# def calculate_aggregate_likes(article_id):
#     # You can get all the likes for the `article_id`
#     # Calculate the aggregate and store in the DB
#     print("#####################################")
#     print("Received {}".format(article_id))
#     print("#####################################")
#     return True

# @celery.task()
# def just_say_hello(name):
#     print("INSIDE TASK")
#     print("Hello {}".format(name))


# @celery.task()
# def print_current_time_job():
#     print("START")
#     now = datetime.now()
#     print("now =", now)
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     print("date and time =", dt_string) 
#     print("COMPLETE")


# @celery.task()
# def long_running_job():
#     print("STARTED LONG JOB")
#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     sse.publish({"message": "STARTED ="+dt_string }, type='greeting')
#     for lp in range(100):
#         now = datetime.now()
#         print("now =", now)
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         sse.publish({"message": "RUNNING ="+dt_string }, type='greeting')
#         print("date and time =", dt_string) 
#         time.sleep(2)

#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")        
#     sse.publish({"message": "COMPLETE ="+dt_string }, type='greeting')
#     print("COMPLETE LONG RUN")

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
        app.run(debug=True)
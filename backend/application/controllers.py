
from flask import render_template,send_file
from main import app as app

from application import tasks
from flask_sse import sse

print("in controller app", app)


@app.route("/export_csv_theatre/<theatre_id>", methods=["GET", "POST"])
def export_csv_theatre(theatre_id):
    
    task =  tasks.export_csv_theatres.delay(theatre_id)
    result = task.get()
    if(result is None):
        return {"message" : "theatre not Found"}, 404
    return send_file(result, attachment_filename=f"theatre_{theatre_id}_details.csv", as_attachment=True)


@app.route("/export_csv_movie/<movie_id>", methods=["GET", "POST"])
def export_csv_movie(movie_id):
    
    task =  tasks.export_csv_movies.delay(movie_id)
    result = task.get()
    if(result is None):
        return {"message" : "Movie not Found"}, 404
    return send_file(result, attachment_filename=f"movie_{movie_id}_details.csv", as_attachment=True)

from flask import jsonify, request
from flask import current_app as app
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid
import time
from .database import db
from .models import Users
from flask_jwt_extended import  jwt_required, create_access_token

@app.route('/register/user',methods=["POST"])
@cross_origin()
def register_user():
    data = request.get_json()
    hash_pwd = generate_password_hash(data['password'],method = 'sha256')
    new_user = Users(public_id = str(uuid.uuid4()),name = data['username'],password = hash_pwd,email=data['email'], role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User registered successfully, olli Saranath"})

@app.route('/register/admin',methods=["POST"])
@cross_origin()
def register_admin():
    data = request.get_json()
    hash_pwd = generate_password_hash(data['password'],method = 'sha256')
    new_user = Users(public_id = str(uuid.uuid4()),password = hash_pwd ,name = data['username'],email=data['email'],role='admin')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"Admin registered successfully"})

@app.route("/login",methods=["POST"])
def login():
   
    data = request.get_json()
    print(data)
    # return {"hello" : data.get("username")}
    uname = data.get("username")
    password = data.get("password")
    user = Users.query.filter_by(name=uname).first()
    
    if check_password_hash(user.password,password):
        user.lastseen=time.time()
        db.session.commit()
        access_token = create_access_token(identity= user.public_id,additional_claims  = {'role':user.role})
        return jsonify({"access_token":access_token, "username":user.name,"role":user.role}),200
    else:
        return jsonify({"error":" gundu gundu janani"})


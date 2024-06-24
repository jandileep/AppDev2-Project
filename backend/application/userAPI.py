from flask_restful import Resource
from flask import request
from .models import Users
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended.utils import decode_token
from flask import jsonify, request

class UserApi(Resource):
    @jwt_required()

    def get(self):
        current_user =get_jwt_identity()
        local = request.headers.get("authorization").split()[1]
        user = Users.query.filter_by(public_id = current_user).first()
        if user:
            return {"message":"You are logged in", "username":user.name, "role":user.role,},200
        return {"message":"Janani is gundu"},404
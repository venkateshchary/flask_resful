from flask_jwt_extended import create_access_token
from flask_restful import Api, Resource
from flask import (Blueprint, request)
from flask_api import status
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import time
from datetime import datetime
from .. import db, jwt
from ..models.user import User
from ..models.permissions import Permissions
from ..models.roles import Roles

bp = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(bp)


def check_password(exist_password, password):
    return check_password_hash(exist_password, password)


class Login(Resource):
    """
        restful apis for user login
    """

    def post(self):
        """api for user login"""
        user_vo = request.get_json()
        print("Entry into login method method: request username: {0}".format(user_vo["username"]))
        user_obj = User.query.filter(User.username == user_vo["username"]).first()
        if user_obj is None:
            return "user doesn't exist", status.HTTP_404_NOT_FOUND
        if not check_password(user_obj.password, user_vo["password"]):
            return "password does not match", status.HTTP_401_UNAUTHORIZED
        else:
            role_name = None
            role_obj = Permissions.query.filter(Permissions.user_id == user_obj.id).first()
            if role_obj:
                role_obj_name = Roles.query.get(role_obj.role_id)
                role_name = role_obj_name.role_name
            ret = {'access_token': create_access_token({"username": user_obj.username,
                                                        "account_no": user_obj.account_no,
                                                        "user_id": user_obj.id,
                                                        "role_name": role_name})}
            print(ret)
            return ret, status.HTTP_200_OK


def login_validation(req):
    msg = None
    if "username" not in req.keys():
        msg = "username is required"
    if "password" not in req.keys():
        msg = "password is required"

    return msg


class Register(Resource):

    def post(self):
        user_vo = request.get_json()
        msg = login_validation(user_vo)
        if msg is not None:
            return msg, status.HTTP_400_BAD_REQUEST
        user_obj = User.query.filter(User.username == user_vo["username"]).first()
        if user_obj:
            return "username is already exist", status.HTTP_409_CONFLICT
        else:
            password = user_vo["password"]
            password = generate_password_hash(password)
            datetime_now = datetime.now().date()
            user_obj = User(username=user_vo["username"], password=password,
                            account_no=round(time.time() * 1000),
                            created_date=datetime_now, email=user_vo["email"])
            db.session.add(user_obj)
            db.session.commit()
            return "user is created", status.HTTP_200_OK


api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

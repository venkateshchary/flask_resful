from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Api, Resource
from flask import (Blueprint, request)
from flask_api import status
import time
from .. import db
from ..models.user import User
from ..models.operations import Operations
from ..models.history import OperationsHistory
from .notifications import sender_email

bp = Blueprint('operations', __name__, url_prefix='/operations')
api = Api(bp)


class Deposit(Resource):
    """
        restful apis for deposit
    """

    @jwt_required
    def post(self):
        vo = request.get_json()
        print(vo)
        token = get_jwt_identity()
        print(token)
        operation_obj = Operations.query.filter(Operations.account_no == token["account_no"]).first()
        user_obj = User.query.get(token['id'])
        if operation_obj:
            operation_obj.amount = operation_obj.amount + vo["amount"]
            operation_obj.modified_date_time = str(round(time.time() * 1000))
            db.session.add(operation_obj)
            db.session.commit()
        else:
            operation_obj = Operations(account_no=token["account_no"],
                                       amount=vo["amount"],
                                       modified_date_time=str(round(time.time() * 1000))
                                       )
            db.session.add(operation_obj)
            db.session.commit()
        history = OperationsHistory(account_no=token["account_no"],
                                    created_date_time=str(round(time.time() * 1000)),
                                    remarks="amount {0} is added".format(vo["amount"]))
        db.session.add(history)
        db.session.commit()
        msg = "amount is deposited into account {0}".format(token["account_no"])
        sender_email(user_obj.email, msg)
        return msg, status.HTTP_200_OK


class Withdraw(Resource):

    @jwt_required
    def post(self):
        vo = request.get_json()
        print(vo)
        token = get_jwt_identity()
        print(token)
        operation_obj = Operations.query.filter(Operations.account_no == token["account_no"]).first()
        if operation_obj:
            if operation_obj.amount > 0:
                user_obj = User.query.get(token["id"])
                operation_obj.amount = operation_obj.amount - vo["amount"]
                operation_obj.modified_date_time = str(round(time.time() * 1000))
                db.session.add(operation_obj)
                db.session.commit()
                history = OperationsHistory(account_no=token["account_no"],
                                            created_date_time=str(round(time.time() * 1000)),
                                            remarks="amount {0} is withdrawn".format(vo["amount"]))
                db.session.add(history)
                db.session.commit()
                msg = "amount is withdrawn from account {0}".format(token["account_no"])
                sender_email(user_obj.email, msg)
                return msg, status.HTTP_200_OK
            else:
                return "your balance is Zero", status.HTTP_200_OK
        else:
            return "can't perform operation", status.HTTP_400_BAD_REQUEST


class Enquiry(Resource):

    @jwt_required
    def get(self):
        token = get_jwt_identity()
        operation_obj = Operations.query.filter(Operations.account_no == token["account_no"]).first()
        if operation_obj:
            msg = "amount available {0}".format(operation_obj.amount)
            return msg, status.HTTP_200_OK
        else:
            return "account is not available", status.HTTP_404_NOT_FOUND


api.add_resource(Deposit, "/deposit")
api.add_resource(Withdraw, "/withdraw")
api.add_resource(Enquiry, "/enquiry")

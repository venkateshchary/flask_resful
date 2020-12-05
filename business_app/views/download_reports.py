from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Api, Resource
from flask import (Blueprint, request, send_from_directory)
from flask_api import status
from functools import wraps
import csv
import os
import time
from ..models.user import User
from ..models.history import OperationsHistory
from . import util

bp = Blueprint('download', __name__, url_prefix='/download')
api = Api(bp)


def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_identity()
        if claims['role_name'] != 'manager':
            return 'managers only!', status.HTTP_403_FORBIDDEN
        else:
            return fn(*args, **kwargs)

    return wrapper


class ReportDownload(Resource):

    @jwt_required
    @manager_required
    def get(self):
        user_id = request.args["user_id"]
        user_obj = User.query.get(user_id)
        if user_obj:
            account_no = user_obj.account_no
            operations_h = OperationsHistory.query.filter(OperationsHistory.account_no == account_no).all()
            res = [util.prepare_vo(op) for op in operations_h]
            keys = res[0].keys()
            pwd = os.getcwd()
            file_name = "transactions_{0}.csv".format(time.ctime())
            with open(file_name, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(res)
            return send_from_directory(directory=pwd, filename=file_name)


api.add_resource(ReportDownload, '/transactions')

from flask_restful import Resource
from flask import request
from app.config.success_config import success_config

class BaseHandler(Resource):
    def __init__(self):
        self.request = request
        self.page_no = 1
        self.page_size = 20

    def return_json(self,status=200, data={}, error={} , success={}, header={}):
        status_identifier = status // 10 ** 2 % 10
        try:
            if header and status_identifier==2:
                return {
                    "success": True,
                    "message": success['message'],
                    "data":data
                }, status, header
            elif status_identifier==2:
                return {
                    "success": True,
                    "message": success['message'],
                    "data":data
                }, status
            else:
                return {
                    "success": False,
                    "message": error['message'],
                    "error_code":error['error_code'],
                    "data":data
                }, status
        except Exception as e:
            print(e)


class Ping(BaseHandler):
    def get(self):
        try:
            return success_config[0], 200
        except Exception as e:
            print(e)
            return {"status": "success", "message": "Authentication Microservices running"}, 200


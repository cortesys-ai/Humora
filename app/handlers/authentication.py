from flask import request, make_response, render_template
from app.helpers.date_time import DateTimeHelper
from app.config.success_config import success_config
from app.handlers.base_handler import BaseHandler
from ..helpers.user import UserHelper   

class UserHandler(BaseHandler, UserHelper, DateTimeHelper):
    def post(self):
        try:
            payload = request.get_json()
            name = payload.get('name')
            email = payload.get('email')
            password = payload.get('password')
            role = payload.get('role')

            response = UserHelper.create_user(self,name,email,password,role)
            self.return_json(status=200,data=response.get('data',{}),success=success_config[0])

        except Exception as e:
            print(e)
    
    def get(self):
        try:
            Data = UserHelper.get_user(self)
            return self.return_json(status=200,data=Data,success=success_config[1])
        except Exception as e:
            print(e)

    def put(self):
        try:
            pass
        except Exception as e:
            print(e)
    
    def delete(self):
        try:
            pass
        except Exception as e:
            print(e)


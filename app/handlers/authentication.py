from flask import request, make_response, render_template
from app.helpers.date_time import DateTimeHelper
from app.config.success_config import success_config
from app.handlers.base_handler import BaseHandler
from ..helpers.user import UserHelper   

class UserHandler(BaseHandler, UserHelper, DateTimeHelper):
    def post(self):
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')

            UserHelper.create_user(self,name,email,password,role)
            self.return_json(status=200,data={},success=success_config[0])

        except Exception as e:
            print(e)
    
    def get(self):
        try:
            Data = UserHelper.get_user(self)
            print(Data)
            return self.return_json(status=200,data=Data,success=success_config[0])
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


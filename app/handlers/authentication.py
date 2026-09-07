from flask import request, make_response, render_template
from app.helpers.date_time import DateTimeHelper
from app.config.success_config import success_config
from app.handlers.base_handler import BaseHandler
from ..helpers.user import UserHelper   
from app.helpers.base_helper import authenticate, generate_jwt_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app.helpers.validation import validate_email, valdate_integer
from app.helpers.base_helper import ApiException
from app.config.error_config import error_config

class UserHandler(BaseHandler, UserHelper, DateTimeHelper):
    # @authenticate
    def post(self):
        try:
            payload = request.get_json()
            name = payload.get('name')
            email = payload.get('email')
            password = payload.get('password')
            role = payload.get('role')

            # if not name :
            #     raise ApiException(error_config[3])

        
            encrypted_password = generate_password_hash(password)

            response = UserHelper.create_user(self,name,email,encrypted_password,role)
            return self.return_json(status=200,data={},success=success_config[2])
        except ApiException:
            return self.return_json(status=400,data={},error=error_config[3])
        except Exception as e:
            return self.return_json(status=400,data={},error=error_config[7])

    @authenticate
    def get(self):
        try:
            Data = UserHelper.get_user(self)
            return self.return_json(status=200,data=Data,success=success_config[1])
        except Exception as e:
            print(e)

    @authenticate
    def put(self):
        try:
            pass
        except Exception as e:
            print(e)

    @authenticate
    def delete(self):
        try:
            pass
        except Exception as e:
            print(e)

class UserLogin(BaseHandler, UserHelper, DateTimeHelper):
    def post(self):
        try:
            payload = request.get_json()
            email = payload.get('email',None).strip().lower()
            password = payload.get('password',None)

            # 1. Look up user by email
            user = User.query.filter_by(email=email).first()

            # 2. Verify existence and password hash
            if not user or not check_password_hash(user.password, password):
                return {
                    "status": "error",
                    "message": "Invalid email or password"
                }, 401

            # 3. Check if account is active
            if user.is_active != 1 or user.status != 1:
                return {
                    "status": "error",
                    "message": "Account is inactive or suspended"
                }, 403

            # 4. Generate JWT
            token = generate_jwt_token(user)

            return {
                "status": "success",
                "message": "Login successful",
                "access_token": token,
                "token_type": "Bearer",
                "user": {
                    "uuid": user.uuid,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            }, 200
        except Exception as e:
            print(e)
            print(
                type(e).__name__,          # TypeError
                __file__,                  # /tmp/example.py
                e.__traceback__.tb_lineno  # 2
            )
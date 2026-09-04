from app import db
from app.helpers.date_time import DateTimeHelper
import uuid
from app.models.user import User
from app.config.success_config import success_config

class UserHelper:
    def create_user(self,name,email,password,role):
        response = success_config[1]
        try:
            
            user = User(name=name,email=email,password=password,role=role,uuid=str(uuid.uuid4()))
            db.session.add(user)
            db.session.commit()
            print(user)
            response['data'] = None
            return None
        except Exception as e:
            print(e)

    def get_user(self):
        try:
            all_data = db.session.query(User.id,User.created_at,User.updated_at,User.uuid,User.email,User.name,User.role).all()
            print(all_data)
            all_data_list = []
            for row in all_data:
                row = DateTimeHelper.make_epoch(self,row)
                all_data_list.append(row)
            return all_data_list
        except Exception as e:
            print(e)
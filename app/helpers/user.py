from app import db
from app.helpers.date_time import DateTimeHelper
import uuid
from app.models.user import User

class UserHelper:
    def create_user(self,name,email,password,role):
        try:
            user = User(name=name,email=email,password=password,role=role,uuid=str(uuid.uuid4()))
            db.session.add(user)
            db.session.commit()
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
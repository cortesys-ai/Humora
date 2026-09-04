from app import api
from app.handlers.authentication import UserHandler
from app.handlers.base_handler import Ping

api.add_resource(UserHandler,'/auth/user')
api.add_resource(Ping,'/auth/ping')
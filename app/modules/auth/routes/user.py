from app import api
from app.modules.auth.handler.authentication import UserHandler

api.add_resource(UserHandler,'/auth/user')
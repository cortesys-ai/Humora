from app import api
from app.handlers.authentication import UserHandler, UserLogin
from app.handlers.base_handler import Ping, AuditLogHandler

api.add_resource(UserHandler,'/auth/user')
api.add_resource(Ping,'/auth/ping')
api.add_resource(AuditLogHandler,'/logs')
api.add_resource(UserLogin,'/auth/login')
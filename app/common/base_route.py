from app import api
from .base_handler import Ping

api.add_resource(Ping,'/auth/ping')
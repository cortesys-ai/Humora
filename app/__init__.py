from flask import Flask, Blueprint
from flask_restful import Api
from app.models.base_model import db, ma, migrate
from app.config import Config
from flasgger import Swagger

flask_app = Flask(__name__, instance_relative_config=True)
flask_app.config.from_object(Config)

swagger = Swagger(flask_app, template_file='openapi.yml')

api_bp = Blueprint('api',__name__)
api = Api(api_bp)
flask_app.register_blueprint(api_bp,url_prefix='/api')

# initialize sqlalchemy
db.init_app(flask_app)

# initialize marshmellow
ma.init_app(flask_app)

# initialize flask migrations
migrate.init_app(flask_app,db)

from app.urls import *

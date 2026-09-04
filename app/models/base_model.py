from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declared_attr

migrate = Migrate(compare_tyoe=True)
ma = Marshmallow()
db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer,primary_key=True)
    created_at = db.Column(db.TIMESTAMP,server_default = db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP,server_default = db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
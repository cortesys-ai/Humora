from app.config import Config
from ....models.base_model import Base, db

class User(Base):
    __tablename__ = Config.TABLE_PREFIX +"user"

    uuid = db.Column(db.String(100))
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    is_active = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(db.Integer, nullable=False, default=0)

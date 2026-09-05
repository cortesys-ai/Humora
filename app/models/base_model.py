from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

migrate = Migrate(compare_tyoe=True)
ma = Marshmallow()
db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer,primary_key=True)
    created_at = db.Column(db.TIMESTAMP,server_default = db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP,server_default = db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)


class ApiAuditLog(Base):
    __tablename__ = "api_audit_logs"

    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    ip_address = db.Column(db.String(45))
    request_headers = db.Column(db.Text)
    request_body = db.Column(db.Text)
    response_body = db.Column(db.Text)
    status_code = db.Column(db.Integer)
    duration_ms = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "endpoint": self.endpoint,
            "method": self.method,
            "ip_address": self.ip_address,
            "request_headers": self.request_headers,
            "request_body": self.request_body,
            "response_body": self.response_body,
            "status_code": self.status_code,
            "duration_ms": self.duration_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
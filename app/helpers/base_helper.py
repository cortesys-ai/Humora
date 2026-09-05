from functools import wraps
from flask import request, current_app
import jwt
from app.config.error_config import error_config
import time
import json
from flask import request, g
from app.models.base_model import ApiAuditLog
from app import db

from datetime import datetime, timedelta, timezone
from flask import current_app
import jwt
from app.config import Config

def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        # 1. Check if Authorization header exists
        if not auth_header:
            return error_config[1], 401

        # 2. Check format: "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return error_config[2], 401

        token = parts[1]

        # 3. Validate & decode the JWT token
        try:
            secret_key = current_app.config.get("SECRET_KEY", "fallback-secret-key")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            # Pass the decoded payload (or user id) into the endpoint via kwargs
            kwargs["current_user"] = payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid or corrupted token"}, 401

        return f(*args, **kwargs)

    return decorated


# Exclude log-fetching APIs and documentation assets from logging
EXCLUDED_PATHS = ["/api/v1/logs", "/apidocs", "/flasgger_static", "/apispec_1.json"]

def register_request_loggers(app):
    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def log_request_response(response):
        # Prevent self-logging loops
        if any(request.path.startswith(path) for path in EXCLUDED_PATHS):
            return response

        duration = (time.time() - g.get("start_time", time.time())) * 1000

        # Extract payload safely (skip binary/upload payloads)
        req_body = None
        if request.is_json:
            req_body = json.dumps(request.get_json(silent=True))
        elif request.form:
            req_body = json.dumps(request.form.to_dict())

        # Extract response payload
        res_body = None
        if response.content_type == "application/json":
            res_body = response.get_data(as_text=True)

        # Sanitize headers (e.g., redact secrets if desired)
        headers_dict = dict(request.headers)
        if "Authorization" in headers_dict:
            headers_dict["Authorization"] = "[REDACTED]"

        log_entry = ApiAuditLog(
            endpoint=request.path,
            method=request.method,
            ip_address=request.remote_addr,
            request_headers=json.dumps(headers_dict),
            request_body=req_body,
            response_body=res_body,
            status_code=response.status_code,
            duration_ms=round(duration, 2)
        )

        try:
            db.session.add(log_entry)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return response


def generate_jwt_token(user):
    try:
        payload = {
            "sub": str(user.uuid),
            "email": str(user.email),
            "name": str(user.name),
            "role": str(user.role),
            "is_active": str(user.is_active),
            "iat": datetime.now(),
            "exp": datetime.now() + timedelta(hours=24)  # 24-hour validity
        }
        # payload = json.dumps(payload)
        print(payload)
        secret_key = current_app.config.get("SECRET_KEY", Config.JWT_SECRET_KEY)
        return jwt.encode(payload, str(secret_key), algorithm="HS256")
    except Exception as e:
        print(e)
        print(
            type(e).__name__,          # TypeError
            __file__,                  # /tmp/example.py
            e.__traceback__.tb_lineno  # 2
        )
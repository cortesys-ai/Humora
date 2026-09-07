from flask_restful import Resource
from flask import request, Response
from app.config.success_config import success_config
from app.models.base_model import ApiAuditLog
from flask import render_template
from app import db

class BaseHandler(Resource):
    def __init__(self):
        self.request = request
        self.page_no = 1
        self.page_size = 20

    def return_json(self,status=200, data={}, error={} , success={}, header={}):
        status_identifier = status // 10 ** 2 % 10
        try:
            if header and status_identifier==2:
                return {
                    "success": True,
                    "message": success['message'],
                    "data":data
                }, status, header
            elif status_identifier==2:
                return {
                    "success": True,
                    "message": success['message'],
                    "data":data
                }, status
            else:
                return {
                    "success": False,
                    "message": error['message'],
                    "code":error['code'],
                    "data":data
                }, status
        except Exception as e:
            print(e)


class Ping(BaseHandler):
    def get(self):
        try:
            return success_config[0], 200
        except Exception as e:
            print(e)
            return {"status": "success", "message": "Authentication Microservices running"}, 200

class AuditLogHandler(BaseHandler):
    def get(self):
        try:
            page = request.args.get("page", 1, type=int)
            per_page = 25

            query = ApiAuditLog.query

            search = request.args.get("search", "").strip()
            method = request.args.get("method", "").strip()
            status = request.args.get("status", "").strip()

            if search:
                query = query.filter(
                    db.or_(
                        ApiAuditLog.endpoint.ilike(f"%{search}%"),
                        ApiAuditLog.ip_address.ilike(f"%{search}%")
                    )
                )

            if method:
                query = query.filter(
                    ApiAuditLog.method == method
                )

            if status == "2xx":
                query = query.filter(
                    ApiAuditLog.status_code.between(200, 299)
                )

            elif status == "4xx":
                query = query.filter(
                    ApiAuditLog.status_code.between(400, 499)
                )

            elif status == "5xx":
                query = query.filter(
                    ApiAuditLog.status_code.between(500, 599)
                )

            logs = query.order_by(
                ApiAuditLog.created_at.desc()
            ).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            total_logs = ApiAuditLog.query.count()

            successful_logs = ApiAuditLog.query.filter(
                ApiAuditLog.status_code.between(200, 399)
            ).count()

            client_errors = ApiAuditLog.query.filter(
                ApiAuditLog.status_code.between(400, 499)
            ).count()

            server_errors = ApiAuditLog.query.filter(
                ApiAuditLog.status_code.between(500, 599)
            ).count()

            html = render_template(
                "logs.html",
                logs=logs,
                total_logs=total_logs,
                successful_logs=successful_logs,
                client_errors=client_errors,
                server_errors=server_errors
            )

            return Response(
                html,
                status=200,
                content_type="text/html; charset=utf-8"
            )

        except Exception as e:
            print(e)
            print(
                type(e).__name__,          # TypeError
                __file__,                  # /tmp/example.py
                e.__traceback__.tb_lineno  # 2
            )
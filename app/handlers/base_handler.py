from flask_restful import Resource
from flask import request
from app.config.success_config import success_config
from app.models.base_model import ApiAuditLog
from flask import render_template

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
                    "error_code":error['error_code'],
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
            per_page = request.args.get("per_page", 20, type=int)
            method = request.args.get("method", type=str)
            status = request.args.get("status_code", type=int)

            query = ApiAuditLog.query

            if method:
                query = query.filter(ApiAuditLog.method == method.upper())
            if status:
                query = query.filter(ApiAuditLog.status_code == status)

            paginated_logs = query.order_by(ApiAuditLog.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )

            # return {
            #     "total": paginated_logs.total,
            #     "page": paginated_logs.page,
            #     "pages": paginated_logs.pages,
            #     "per_page": paginated_logs.per_page,
            #     "data": [log.to_dict() for log in paginated_logs.items]
            # }, 200
            return render_template("logs.html")
        except Exception as e:
            print(e)
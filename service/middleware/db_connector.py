from database import db
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            db.connect()
            response = await call_next(request)
        except Exception as e:
            print(e)
        finally:
            db.close()

        return response

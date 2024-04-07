from fastapi import APIRouter
from fastapi.responses import FileResponse

from service import file_service


file_router = APIRouter(prefix="/files", tags=["files"])


@file_router.get("/file/{file_id}")
async def get_file(file_id):
    url, filename = await file_service.get_file(file_id)
    return FileResponse(url)

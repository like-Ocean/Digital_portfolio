from fastapi import APIRouter, Depends, Response
from service import comment_service
from models import User
from service.user_service import get_current_user
from .comment_scheme import SendCommentModel, DeleteCommentModel


comment_router = APIRouter(prefix="/comments", tags=["comments"])


@comment_router.post("/send")
async def create(data: SendCommentModel, current_user: User = Depends(get_current_user)):
    comment = await comment_service.send_comment(data.user_id, data.project_id, data.comment)
    return comment


@comment_router.get("/projects/project/{project_id}")
async def get_project_comments(project_id):
    comments = await comment_service.get_project_comments(project_id)
    return comments


@comment_router.delete("/comment/delete")
async def delete_my_comment(data: DeleteCommentModel, current_user: User = Depends(get_current_user)):
    await comment_service.delete_comment(data.user_id, data.comment_id)
    return Response(status_code=204)

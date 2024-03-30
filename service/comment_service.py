from datetime import datetime
from fastapi import HTTPException
from database import objects
from models import User, Comment, Project


async def send_comment(user_id: int, project_id: int, comment: str):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    project = await objects.get_or_none(Project.select().where(Project.id == project_id))
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    comment = await objects.create(
        Comment,
        project=project,
        user=user,
        comment=comment,
        post_date=datetime.now()
    )

    return comment.get_dto()


async def get_project_comments(project_id: int):
    comments = await objects.execute(Comment.select().where(Comment.project == project_id))
    return [comment.get_dto() for comment in comments]


async def delete_comment(user_id: int, comment_id: int):
    comment = await objects.get_or_none(Comment.select().where(
        (Comment.id == comment_id) & (Comment.user == user_id)
    ))
    await objects.delete(comment)


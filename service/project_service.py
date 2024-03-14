from datetime import datetime
from fastapi import HTTPException, UploadFile
from database import objects
from models import User, Project, ProjectFile
from service import file_service


async def create_project(user_id: int, name: str, description: str):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    project = await objects.create(
        Project,
        user=user_id,
        name=name,
        description=description,
        creation_date=datetime.now()
    )
    return project.get_dto()


async def change_project(project_id: int, name: str, description: str):
    project = await objects.get_or_none(Project.select().where(Project.id == project_id))
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    project.name = name
    project.description = description

    await objects.update(project)

    return project.get_dto()


async def delete(project_id: int, user_id: int):
    project = await objects.get_or_none(Project.select().where(Project.id == project_id))
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    if project.user.id != user_id:
        raise HTTPException(status_code=403, detail="You can't to delete this project")

    project = Project.delete().where(Project.id == project_id)
    await objects.execute(project)


async def get_all_projects():
    projects = await objects.execute(Project.select())
    return [project.get_dto() for project in projects]


# МБ эту функцию нужно будет убрать от сюда
async def get_user_projects(user_id: int):
    projects = await objects.execute(Project.select().where(Project.user == user_id))
    return [project.get_dto() for project in projects]


async def get_project(project_id: int):
    projects = await objects.execute(Project.select().where(Project.id == project_id))
    return [project.get_dto() for project in projects]

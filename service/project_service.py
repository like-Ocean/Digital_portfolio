from datetime import datetime

from fastapi import HTTPException, UploadFile

from database import objects
from models import User, Project, ProjectFile, File, Category
from service import file_service


async def create_project(user_id: int, name: str, description: str, category_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    project = await objects.create(
        Project,
        user=user_id,
        name=name,
        description=description,
        creation_date=datetime.now(),
        category=category_id
    )

    files = await objects.execute(
        ProjectFile.select().where(ProjectFile.project == project)
    )

    return {**project.get_dto(), 'files': [file.get_dto() for file in files]}


async def change_project(project_id: int, name: str, description: str, category_id: int):
    project = await objects.get_or_none(Project.select().where(Project.id == project_id))
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    project.name = name or project.name
    project.description = description or project.description
    project.category = category_id or project.category

    await objects.update(project)

    files = await objects.execute(
        ProjectFile.select().where(ProjectFile.project == project)
    )

    return {**project.get_dto(), 'files': [file.get_dto() for file in files]}


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

    result_data = []

    for project in projects:
        files = await objects.execute(ProjectFile.select().where(ProjectFile.project == project.id))
        project_dto = project.get_dto()
        project_dto['files'] = [file.get_dto() for file in files]
        result_data.append(project_dto)

    return result_data


async def get_user_projects(user_id: int):
    projects = await objects.execute(Project.select().where(Project.user == user_id))

    result_data = []

    for project in projects:
        files = await objects.execute(ProjectFile.select().where(ProjectFile.project == project.id))
        project_dto = project.get_dto()
        project_dto['files'] = [file.get_dto() for file in files]
        result_data.append(project_dto)

    return result_data


async def get_project(project_id: int):
    project = await objects.get_or_none(Project.select().where(Project.id == project_id))
    project_files = await objects.execute(
        ProjectFile.select().where(ProjectFile.project == project_id)
    )
    return {**project.get_dto(), 'files': [file.get_dto() for file in project_files]}


async def save_project_files(files: [UploadFile], project_id: int):
    project = await objects.get_or_none(Project.select().where(Project.id == project_id))
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    files_list = []

    for file in files:
        saved_file = await file_service.save_file(file)
        files_list.append(saved_file)

    for document in files_list:
        await objects.create(ProjectFile, project=project, file=document.id)

    return {**project.get_dto(), 'files': [doc.get_dto() for doc in files_list]}


async def delete_file(file_id: str, project_id: int):
    project_file = await objects.get_or_none(ProjectFile.select().where(
        (ProjectFile.project == project_id) & (ProjectFile.file == file_id)
    ))
    await objects.execute(ProjectFile.delete().where(ProjectFile.id == project_file))
    await objects.execute(File.delete().where(File.id == file_id))


async def get_category_projects(category_id: int):
    projects = await objects.execute(Project.select().where(Project.category == category_id))

    result_data = []

    for project in projects:
        files = await objects.execute(ProjectFile.select().where(ProjectFile.project == project.id))
        project_dto = project.get_dto()
        project_dto['files'] = [file.get_dto() for file in files]
        result_data.append(project_dto)

    return result_data


async def get_all_categories():
    categories = await objects.execute(Category.select())
    return [category.get_dto() for category in categories]


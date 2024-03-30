from typing import List

from fastapi import APIRouter, Response, UploadFile, Depends

from models import User
from service import project_service
from service.user_service import get_current_user
from .project_scheme import CreateProjectModel, ChangeProjectModel, DeleteProjectModel, DeleteFileModel

project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.post("/create")
async def create(project: CreateProjectModel, current_user: User = Depends(get_current_user)):
    project_data = await project_service.create_project(
        project.user_id,
        project.name,
        project.description,
    )
    return project_data


@project_router.patch("/change")
async def change_project(project: ChangeProjectModel, current_user: User = Depends(get_current_user)):
    project_data = await project_service.change_project(
        project.project_id,
        project.name,
        project.description
    )
    return project_data


@project_router.delete("/project/delete/{project_id}")
async def delete_project(data: DeleteProjectModel, project_id,
                         current_user: User = Depends(get_current_user)):
    await project_service.delete(project_id, data.user_id)
    return Response(status_code=204)


@project_router.get("/")
async def get_all_project():
    return await project_service.get_all_projects()


# когда нужно отобразить все проекты пользователя в его профиле
@project_router.get("/user/{user}")
async def get_user_projects(user):
    return await project_service.get_user_projects(user)


# когда нужно отобразить детали конкретного проекта, на отдельной странице проекта.
@project_router.get("/project/{project_id}")
async def get_project(project_id):
    return await project_service.get_project(project_id)


@project_router.post("/project/file/upload")
async def upload_files(files: List[UploadFile], project_id,
                       current_user: User = Depends(get_current_user)):
    file_data = await project_service.save_project_files(files, project_id)
    return file_data


# Сделать так чтобы project_id был в Request body
@project_router.delete("/project/file/delete")
async def delete_file(file: DeleteFileModel, current_user: User = Depends(get_current_user)):
    await project_service.delete_file(file.file_id, file.project_id)
    return Response(status_code=204)

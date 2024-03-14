from fastapi import APIRouter, Response
from .project_scheme import CreateProjectModel, ChangeProjectModel, DeleteProjectModel
from service import project_service

project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.post("/create")
async def create(project: CreateProjectModel):
    project_data = await project_service.create_project(
        project.user_id,
        project.name,
        project.description,
    )
    return project_data


@project_router.patch("/change")
async def change_project(project: ChangeProjectModel):
    project_data = await project_service.change_project(
        project.project_id,
        project.name,
        project.description
    )
    return project_data


# user_id брать из localStorage
@project_router.delete("/project/delete/{project_id}")
async def delete_project(data: DeleteProjectModel, project_id):
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

# то что нужно но надо понять как работает
# @project_router.post("/files/")
# async def create_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}

# @project_router.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     return await save_file(file)

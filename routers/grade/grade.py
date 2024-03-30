from fastapi import APIRouter, Depends
from models import User
from service.user_service import get_current_user
from service import grade_service
from .grade_scheme import *


grade_router = APIRouter(prefix="/grades", tags=["grades"])


@grade_router.post("/grade/add")
async def add_grade(grade: AddGradeModel, current_user: User = Depends(get_current_user)):
    grade_data = await grade_service.add_grade(grade.user_id, grade.project_id, grade.grade)
    return grade_data


@grade_router.get("/")
async def get_all_grades():
    return await grade_service.get_all_grades()


@grade_router.get("/project/{project_id}")
async def get_project_grades(project_id):
    return await grade_service.get_project_grades(project_id)


@grade_router.get("/project/{project_id}/average/grade")
async def get_avg_project_grade(project_id):
    grade_data = await grade_service.get_average_grade(project_id)
    return grade_data


@grade_router.get("/projects/sorted/by_rating")
async def sort_project_by_rating():
    return await grade_service.get_projects_sorted_by_rating()
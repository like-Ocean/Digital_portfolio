from fastapi import HTTPException
from peewee import fn

from database import objects
from models import Project, Grade


async def add_grade(user_id: int, project_id: int, grade: float):
    project = await objects.get_or_none(Project.select().where(Project.id == project_id))
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    grade = await objects.create(
        Grade,
        project=project_id,
        user=user_id,
        grade=grade
    )

    return grade.get_dto()


async def get_all_grades():
    grades = await objects.execute(Grade.select())
    return [grade.get_dto() for grade in grades]


async def get_project_grades(project_id: int):
    grades = await objects.execute(Grade.select().where(Grade.project == project_id))
    return [grade.get_dto() for grade in grades]


async def get_project_user_grades(user_id: int, project_id: int):
    grade = await objects.get_or_none(Grade.select().where(
        (Grade.user == user_id) & (Grade.project == project_id)
    ))
    if not grade:
        return HTTPException(status_code=400, detail="Grade not found")
    return grade.get_dto()


async def get_average_grade(project_id: int):
    average_grade = await objects.get(
        Grade.select(fn.AVG(Grade.grade)).where(Grade.project == project_id)
    )
    return {"average_grade": average_grade.avg}


async def get_projects_sorted_by_rating():
    projects = await objects.execute(
        Project.select().join(Grade).group_by(Project.id).order_by(fn.AVG(Grade.grade).desc())
    )
    return [project.get_dto() for project in projects]

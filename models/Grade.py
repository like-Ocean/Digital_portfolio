from peewee import AutoField, ForeignKeyField, FloatField
from database import BaseModel
from models import User, Project


class Grade(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    grade = FloatField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'project': {
                'id': self.project.id,
                'name': self.project.name,
                'description': self.project.description,
            },
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'surname': self.user.surname
            },
            'grade': self.grade
        }

    class Meta:
        db_table = 'grades'
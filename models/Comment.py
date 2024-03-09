from peewee import AutoField, ForeignKeyField, TextField, DateField
from database import BaseModel
from models import User, Project


class Comment(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    comment = TextField(null=False)
    post_date = DateField()

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
            'comment': self.comment,
            'post_date': self.post_date,
        }

    class Meta:
        db_table = 'comments'
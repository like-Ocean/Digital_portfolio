from peewee import TextField, AutoField, DateField, ForeignKeyField
from database import BaseModel
from models import User


class Project(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    name = TextField(null=False)
    description = TextField(null=True)
    creation_date = DateField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'surname': self.user.surname
            },
            'name': self.name,
            'description': self.description,
            'creation_date': self.creation_date
        }

    class Meta:
        db_table = 'projects'

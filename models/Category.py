from peewee import CharField, AutoField
from database import BaseModel


class Category(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    name = CharField(null=False, unique=True, max_length=255)

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name
        }

    class Meta:
        db_table = 'categories'

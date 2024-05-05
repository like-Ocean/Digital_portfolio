from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel
from models import File


class User(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    login = TextField(null=False, unique=True)
    email = TextField(null=False)
    first_name = TextField(null=False)
    surname = TextField(null=False)
    country = TextField(null=False)
    city = TextField(null=False)
    avatar = ForeignKeyField(File, on_delete='CASCADE', null=True)
    password = TextField(null=False)
    phone = TextField(null=True)
    about = TextField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'first_name': self.first_name,
            'surname': self.surname,
            'country': self.country,
            'city': self.city,
            'avatar': self.avatar.get_dto() if self.avatar else None,
            'phone': self.phone,
            'about': self.about
        }

    class Meta:
        db_table = 'users'

from peewee import TextField, AutoField, IntegerField
from database import BaseModel


class User(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    login = TextField(null=False, unique=True)
    email = TextField(null=False)
    first_name = TextField(null=False)
    surname = TextField(null=False)
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
            'phone': self.phone,
            'about': self.about
        }

    class Meta:
        db_table = 'users'

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
    subscribers_count = IntegerField(default=0)
    subscriptions_count = IntegerField(default=0)

    def get_dto(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'first_name': self.first_name,
            'surname': self.surname,
            'phone': self.phone,
            'about': self.about,
            'subscribers_count': self.subscribers_count,
            'subscriptions_count': self.subscriptions_count
        }

    class Meta:
        db_table = 'users'

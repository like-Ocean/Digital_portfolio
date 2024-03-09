from models import User
from peewee import AutoField, ForeignKeyField, TextField
from database import BaseModel


class Session(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user = ForeignKeyField(User, backref='sessions', on_delete='CASCADE', null=False)
    session = TextField(null=False)

    class Meta:
        db_table = 'sessions'
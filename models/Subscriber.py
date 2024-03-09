from models import User
from peewee import AutoField, ForeignKeyField
from database import BaseModel


class Subscriber(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user = ForeignKeyField(User, backref='subscriptions')
    subscriber = ForeignKeyField(User, backref='subscribers')

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'surname': self.user.surname
            },
            'subscriber': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'surname': self.user.surname
            },
        }

    class Meta:
        db_table = 'subscribers'


# User1 подписался на User2
# id:1 user:2 subscriber:1

# User2 подписался на User1
# id:2 user:2 subscriber:1

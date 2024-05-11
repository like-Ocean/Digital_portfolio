from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel
from models import User, File


class Certificate(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user = ForeignKeyField(User, backref='certificates', on_delete='CASCADE', null=False)
    name = TextField(null=False)
    company = TextField(null=True)
    link = TextField(null=True)
    file = ForeignKeyField(File, on_delete='CASCADE', null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'login': self.user.login,
                'first_name': self.user.first_name,
                'surname': self.user.surname,
                'avatar': self.user.avatar.get_dto() if self.user.avatar else None,
            },
            'name': self.name,
            'company': self.company,
            'link': self.link,
            **self.file.get_dto(),
        }

    class Meta:
        db_table = 'certificates'

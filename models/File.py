from peewee import CharField, TextField
from database import BaseModel


class File(BaseModel):
    id = CharField(primary_key=True, unique=True, null=False)
    hash = TextField(null=False)
    url = TextField(null=False)
    filename = TextField(null=False)

    def get_dto(self):
        return {
            'file_id': self.id,
            'filename': self.filename
        }

    class Meta:
        db_table = 'files'

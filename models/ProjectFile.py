from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import Project, File


class ProjectFile(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    file = ForeignKeyField(File, on_delete='CASCADE', null=False)

    def get_dto(self):
        return {
            'project': {
                'id': self.project.id,
                'name': self.project.name,
            },
            **self.file.get_dto(),
        }

    class Meta:
        db_table = 'project_files'

import os
from peewee import Model
from peewee_async import Manager, PooledPostgresqlDatabase
from dotenv import load_dotenv

load_dotenv()

db = PooledPostgresqlDatabase(
    os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('HOST'),
    port=int(os.environ.get('DB_PORT')),
    autoconnect=False,
    autorollback=True,
    max_connections=5,
)
objects = Manager(db)


class BaseModel(Model):
    class Meta:
        database = db

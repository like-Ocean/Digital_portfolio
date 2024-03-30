from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os

from database import db
from service.middleware import DatabaseMiddleware
from models import (User, Session, Category, Project, Grade, Comment, File, ProjectFile, Certificate)
from routers import routes


load_dotenv()

app = FastAPI()

for router in routes:
    app.include_router(router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DatabaseMiddleware)


if __name__ == '__main__':
    with db:
        db.create_tables([
            User, Session, Category, Project, Grade,
            Comment, File, ProjectFile, Certificate
        ])
    uvicorn.run(
        "__index__:app",
        host=os.environ.get("HOST"),
        port=int(os.environ.get("PORT")),
        log_level="debug",
        reload=True
    )



from .user import user
from .project import project

routes = [
    user.user_router,
    project.project_router
]

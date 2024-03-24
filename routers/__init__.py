from .user import user
from .project import project
from .certificate import certificate

routes = [
    user.user_router,
    project.project_router,
    certificate.certificate_router
]

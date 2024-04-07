from .user import user
from .project import project
from .certificate import certificate
from .comment import comment
from .grade import grade
from .file import file

routes = [
    user.user_router,
    project.project_router,
    certificate.certificate_router,
    comment.comment_router,
    grade.grade_router,
    file.file_router
]

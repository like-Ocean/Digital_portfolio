from typing import List

from fastapi import APIRouter, UploadFile, File, Depends, Response, Form

from models import User
from service import certificate_service
from service.user_service import get_current_user
from .certificate_scheme import AddCertificateModel, EditCertificateModel, DeleteCertificateModel

certificate_router = APIRouter(prefix="/certificates", tags=["certificates"])

# @certificate_router.post("/certificate/add")
# async def add_certificate(data: AddCertificateModel = Depends(), file: UploadFile = File(...),
#                           current_user: User = Depends(get_current_user)):
#     certificate = await certificate_service.add_certificate(
#         data.user_id, data.name,
#         data.company, data.link,
#         file
#     )
#     return certificate


@certificate_router.post("/certificate/file/upload")
async def upload_certificate(file: UploadFile, current_user: User = Depends(get_current_user)):
    certificate = await certificate_service.upload_certificate_file(file)
    return certificate


@certificate_router.post("/certificate/v2/add")
async def add_certificate(data: AddCertificateModel,
                                   current_user: User = Depends(get_current_user)):

    certificate = await certificate_service.add_certificate(
        data.user_id, data.name,
        data.company, data.link,
        data.file_id
    )
    return certificate


@certificate_router.patch("/certificate/change")
async def edit_certificate(data: EditCertificateModel,

                           current_user: User = Depends(get_current_user)):
    certificate = await certificate_service.change_certificate(
        data.user_id, data.certificate_id, data.name,
        data.company, data.link
    )
    return certificate


@certificate_router.delete("/certificate/delete")
async def delete_certificate(data: DeleteCertificateModel,
                             current_user: User = Depends(get_current_user)):
    await certificate_service.remove_certificate(data.user_id, data.certificate_id, data.file_id)
    return Response(status_code=204)


@certificate_router.get("/")
async def get_all_certificates():
    certificates = await certificate_service.get_certificates()
    return certificates


@certificate_router.get("/{certificate_id}")
async def get_certificate(certificate_id):
    certificates = await certificate_service.get_certificate(certificate_id)
    return certificates


@certificate_router.get("/user/{user}")
async def get_user_certificates(user):
    certificates = await certificate_service.get_user_certificates(user)
    return certificates




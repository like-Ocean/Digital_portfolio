from .certificate_scheme import AddCertificateModel, EditCertificateModel, DeleteCertificateModel
from fastapi import APIRouter, UploadFile, File, Depends, Response
from service import certificate_service

certificate_router = APIRouter(prefix="/certificates", tags=["certificates"])


# функция выглядит правильно и по сути так и есть, но проблема в том, что при добавленни файлов к проекту
# используется query параметр мб там лучше будет это изменить.

# Тоже работает но, остановился я на другом варианте реализации
# @certificate_router.post("/add")
# async def add_certificate(user_id: int = Form(...), name: str = Form(..., min_length=1),
#                           company: str = Form(None), link: str = Form(None),
#                           file: UploadFile = File(...)):
#     certificate = await certificate_service.add_certificate(
#         user_id, name,
#         company, link,
#         file
#     )
#     return certificate

@certificate_router.post("/certificate/add")
async def add_certificate(data: AddCertificateModel = Depends(), file: UploadFile = File(...)):
    certificate = await certificate_service.add_certificate(
        data.user_id, data.name,
        data.company, data.link,
        file
    )
    return certificate


@certificate_router.patch("/certificate/change")
async def edit_certificate(data: EditCertificateModel = Depends(), file: UploadFile = File(None)):
    certificate = await certificate_service.change_certificate(
        data.certificate_id, data.name,
        data.company, data.link,
        file
    )
    return certificate


@certificate_router.delete("/certificate/delete")
async def delete_certificate(data: DeleteCertificateModel):
    await certificate_service.remove_certificate(data.certificate_id, data.file_id)
    return Response(status_code=204)


@certificate_router.get("/")
async def get_all_certificates():
    certificates = await certificate_service.get_certificates()
    return certificates


@certificate_router.get("/{certificate_id}")
async def get_certificate(certificate_id):
    certificates = await certificate_service.get_certificate(certificate_id)
    return certificates




from fastapi import HTTPException, UploadFile
from database import objects
from models import User, Certificate, File
from service import file_service


async def add_certificate(user_id: int, name: str, company: str, link: str, file: UploadFile):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    file_id = await file_service.save_file(file)

    certificate = await objects.create(
        Certificate,
        user=user_id,
        name=name,
        company=company,
        link=link,
        file=file_id
    )
    return certificate.get_dto()


async def change_certificate(certificate_id: int, name: str, company: str, link: str, file: UploadFile = None):
    certificate = await objects.get_or_none(Certificate.select().where(Certificate.id == certificate_id))
    if not certificate:
        raise HTTPException(status_code=400, detail="Certificate not found")

    if file:
        file_id = await file_service.save_file(file)
        certificate.file = file_id

    certificate.name = name or certificate.name
    certificate.company = company or certificate.company
    certificate.link = link or certificate.link

    await objects.update(certificate)

    return certificate.get_dto()


async def remove_certificate(certificate_id: int, file_id: str):
    await objects.execute(Certificate.delete().where(Certificate.id == certificate_id))
    await objects.execute(File.delete().where(File.id == file_id))


async def get_certificates():
    certificates = await objects.execute(Certificate.select())
    return [certificate.get_dto() for certificate in certificates]


async def get_certificate(certificate_id: int):
    certificate = await objects.get_or_none(Certificate.select().where(Certificate.id == certificate_id))
    if not certificate:
        raise HTTPException(status_code=400, detail="Certificate not found")

    return certificate.get_dto()

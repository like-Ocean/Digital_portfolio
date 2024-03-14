import hashlib
import os
from uuid import uuid4
from fastapi import UploadFile
from database import objects
from models import File
import magic
from pathlib import Path

DOCUMENT_EXT = ['.docx', '.doc', '.txt', '.pptx', '.ppt', '.pdf']
IMAGE_EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
ARCHIVE_EXT = ['.rar', '.zip', '.7z']


async def get_file_type(file: UploadFile):
    header = await file.read(1024)
    await file.seek(0)
    file_format = magic.from_buffer(header, mime=True).split('/')
    return file_format[0]


async def get_file_hash(file: UploadFile):
    sha1sum = hashlib.sha1()
    chunk = await file.read(2 ** 16)
    while len(chunk) != 0:
        sha1sum.update(chunk)
        chunk = await file.read(2 ** 16)
    await file.seek(0)
    return sha1sum.hexdigest()


def get_file_ext(filename: str):
    split_name = filename.split('.')
    return '.' + split_name[-1] if len(split_name) >= 2 else ''


def get_folder(file_type: str, file_ext: str):
    if file_type == 'application' and file_ext in DOCUMENT_EXT:
        folder = 'documents'
    elif file_type == 'image':
        folder = 'images'
    else:
        folder = 'others'
    full_path = os.path.join(os.environ.get("USER_FILES_FOLDER"), folder)
    Path(full_path).mkdir(parents=True, exist_ok=True)
    return folder


async def save_file(file: UploadFile):
    file_hash = await get_file_hash(file)
    file_type = await get_file_type(file)
    file_ext = get_file_ext(file.filename)
    folder = get_folder(file_type, file_ext)

    exist_file = await objects.get_or_none(File, hash=file_hash)

    if not exist_file:
        user_files_folder = os.environ.get("USER_FILES_FOLDER")
        url = f'{folder}/{file_hash + get_file_ext(file.filename)}'
        with open(f'{user_files_folder}/{url}', 'wb') as out_file:
            content = await file.read()
            out_file.write(content)
    else:
        url = exist_file.url

    new_file = await objects.create(
        File,
        id=str(uuid4()),
        hash=file_hash,
        url=url,
        filename=file.filename
    )
    return new_file

import re
from uuid import uuid4

from fastapi import HTTPException, Request
from werkzeug.security import generate_password_hash, check_password_hash

from database import objects
from models import User, Session


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not re.search('[A-Z]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
    if not re.search('[0-9]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit")


async def registration(login: str, email: str, first_name: str, surname: str, password: str):
    if await objects.count(User.select().where(User.login == login)) > 0:
        raise HTTPException(status_code=400, detail="Login already exists")

    validate_password(password)

    user = await objects.create(
        User,
        login=login,
        email=email,
        first_name=first_name,
        surname=surname,
        password=generate_password_hash(password)
    )
    user = await objects.get_or_none(User.select().where(User.id == user.id))
    return user.get_dto()


async def authorization(login: str, password: str):
    user = await objects.get_or_none(User.select().where(User.login == login))
    if not user or not check_password_hash(user.password, password):
        raise HTTPException(status_code=400, detail="Wrong login or password")

    user_sessions = await objects.execute(Session.select().where(Session.user == user))

    if len(user_sessions) >= 5:
        oldest_session = min(user_sessions, key=lambda session: session.id)
        await objects.delete(oldest_session)

    session = await objects.create(Session, user=user, session=str(uuid4()))
    return user.get_dto(), session.session


# TODO: if not session ошибка нужно if len(sessions) <= 0
async def authorization_check(session: str):
    sessions = await objects.execute(Session.select().where(Session.session == session))
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    session = sessions[0]

    users = await objects.execute(User.select().where(User.id == session.user))
    if not users:
        raise HTTPException(status_code=403, detail="Forbidden")

    return users[0].get_dto()


async def get_current_user(request: Request):
    user_session = request.cookies.get('session')
    if not user_session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = await objects.get(Session.select().where(Session.session == user_session))
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await objects.get(User.select().where(User.id == session.user))
    return user


async def change_user(user_id: int, login: str, email: str,
                      first_name: str, surname: str, phone: str, about: str):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if await objects.count(User.select().where((User.login == login) & (User.id != user_id))) > 0:
        raise HTTPException(status_code=400, detail="User with this login already exists")

    user.login = login if login is not None else user.login
    user.email = email or user.email
    user.first_name = first_name or user.first_name
    user.surname = surname or user.surname
    user.phone = phone or user.phone
    user.about = about or user.about

    await objects.update(user)

    return user.get_dto()


async def change_password(user_id: int, password: str):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    validate_password(password)
    user.password = generate_password_hash(password)
    await objects.update(user)


# TODO: убрать из функций удаления проверку на существование объекта и возвращать статус код 204
async def delete(user_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    user = User.delete().where(User.id == user_id)
    await objects.execute(user)


async def get_users():
    users = await objects.execute(User.select())
    return [user.get_dto() for user in users]


async def get_user(user_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return user.get_dto()



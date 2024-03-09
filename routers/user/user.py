from fastapi import APIRouter, Response, Request, HTTPException
from starlette.responses import JSONResponse
from .user_scheme import RegisterModel, ChangeModel, DeleteUserModel, ChangePasswordModel, Authorization
from service import user_service

user_router = APIRouter(prefix="/users")


@user_router.post("/registration")
async def registration(user: RegisterModel):
    user_data = await user_service.registration(
        user.login,
        user.email,
        user.first_name,
        user.surname,
        user.password
    )
    return user_data


@user_router.post("/authorization")
async def authorization(user: Authorization):
    user_data, session = await user_service.authorization(user.login, user.password)
    response = JSONResponse(content=user_data)
    response.set_cookie('session', session, httponly=True)
    return response


@user_router.get("/auth/check")
async def auth_check(request: Request):
    session = request.cookies.get('session')
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await user_service.authorization_check(session)
    return user


@user_router.post("/user/logout")
async def logout():
    response = Response(status_code=200)
    response.set_cookie(key="session", value="", httponly=True)
    return response


@user_router.patch("/user/edit")
async def edit_user(user: ChangeModel):
    user_data = await user_service.change_user(
        user.user_id,
        user.login,
        user.email,
        user.first_name,
        user.surname,
        user.phone,
        user.about
    )
    return user_data


@user_router.patch("/user/edit/password")
async def edit_password(user: ChangePasswordModel):
    await user_service.change_password(user.user_id, user.password)
    return Response(status_code=200)


@user_router.delete("/user/delete")
async def delete_user(user: DeleteUserModel):
    await user_service.delete(user.user_id)
    return Response(status_code=204)


@user_router.get("/")
async def get_all_user():
    user_data = await user_service.get_users()
    return user_data


@user_router.get("/user/{user_id}")
async def get_user(user_id):
    user_data = await user_service.get_user(user_id)
    return user_data


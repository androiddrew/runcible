from typing import List, Union
from molten import Route, Include, HTTP_201, HTTP_202, HTTPError, HTTP_404, HTTP_409
from sqlalchemy.exc import IntegrityError

from runcible.schema import APIResponse
from runcible.error import EntityNotFound
from .model import User
from .manager import UserManager


def create_user(user: User, user_manger: UserManager) -> User:
    try:
        _user = user_manger.create_user(user)
    except IntegrityError as err:
        raise HTTPError(HTTP_409,
                        APIResponse(status=409,
                                    message=f"User email {user.email} or {user.display_name} already in use."))
    headers = {"Location": _user.href}
    return HTTP_201, _user, headers


def get_user_by_display_name(display_name: str, user_manager: UserManager) -> Union[User, APIResponse]:
    try:
        user = user_manager.get_user_by_display_name(display_name)
    except EntityNotFound as err:
        raise HTTPError(HTTP_404,
                        APIResponse(status=404,
                                    message=err.message))
    return user


user_routes = Include("/users", [
    Route("", create_user, method="POST"),
    Route("/{display_name}", get_user_by_display_name, method="GET")
])

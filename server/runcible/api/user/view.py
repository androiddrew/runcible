from typing import Union
from molten import Route, Include, HTTP_201, HTTPError, HTTP_404, HTTP_401, HTTP_403, HTTP_409
from sqlalchemy.exc import IntegrityError
from molten_jwt import JWT, JWTIdentity

from runcible import APIResponse
from runcible.error import EntityNotFound
from .model import User, Login, Token
from .manager import UserManager


def create_user(user: User, user_manger: UserManager) -> User:
    try:
        _user = user_manger.create_user(user)
    except IntegrityError as err:  # noqa: F841
        raise HTTPError(
            HTTP_409,
            APIResponse(
                status=409,
                message=f"User email {user.email} or {user.display_name} already in use.",
            ),
        )
    headers = {"Location": _user.href}
    return HTTP_201, _user, headers


def get_user_by_display_name(
        display_name: str, user_manager: UserManager
) -> Union[User, APIResponse]:
    try:
        user = user_manager.get_user_by_display_name(display_name)
    except EntityNotFound as err:
        raise HTTPError(HTTP_404, APIResponse(status=404, message=err.message))
    return user


def get_auth_token(
        login: Login, user_manger: UserManager, jwt: JWT
) -> Union[Token, APIResponse]:
    """Returns an authorization token on successful login."""
    try:
        user = user_manger.get_usermodel_by_email(login.email)
    except EntityNotFound as err:
        raise HTTPError(HTTP_404, APIResponse(status=404, message=err.message))
    if not user.check_password(login.password):
        raise HTTPError(
            HTTP_401,
            APIResponse(status=401, message="Password provided does not match."),
        )
    token_payload = {"sub": user.id, "email": user.email, "is_admin": user.admin}
    token = jwt.encode(token_payload)
    return Token(status=200, message="Successfully logged in.", auth_token=token)


def get_user_profile(jwt_user: JWTIdentity, user_manager: UserManager) -> Union[User, APIResponse]:
    """Returns an authenticated user's profile information."""
    if jwt_user is None:
        raise HTTPError(HTTP_403, "Forbidden")
    try:
        user = user_manager.get_user_by_email(jwt_user.email)
    except EntityNotFound as err:
        print(err)
        raise HTTPError(HTTP_404, APIResponse(status=404, message=err.message))
    return user


user_routes = Include(
    "/users",
    [
        Route("", create_user, method="POST", name="legacy_user_create"),
        Route("/{display_name}", get_user_by_display_name, method="GET"),
    ],
)

auth_routes = Include(
    "/auth",
    [
        Route("/register", create_user, method="POST"),
        Route("/login", get_auth_token, method="POST"),
        Route("/profile", get_user_profile, method="GET"),
    ],
)

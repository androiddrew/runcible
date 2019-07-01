import bcrypt
from typing import Optional
from molten import schema, field
from sqlalchemy import Column, String, Boolean

from ...db import Base, DBMixin
from runcible import Link, APIResponse
from ...validation import ExtStringValidator

BCRYPT_LOG_ROUNDS = 11


# TODO add a gravatar user icon field
# TODO consider adding last_ip and last_login fields
@schema
class User:
    id: int = field(response_only=True)
    href: Link = field(response_only=True)
    email: str = field(
        validator=ExtStringValidator(),
        pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})",
        pattern_err_msg="Email address verification failed.",
    )
    display_name: Optional[str]
    password: str = field(request_only=True)
    createdDate: str = field(response_only=True)
    modifiedDate: str = field(response_only=True)
    confirmed: bool = field(response_only=True)
    active: bool = field(response_only=True)


@schema
class Login:
    email: str = field(
        validator=ExtStringValidator(),
        pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})",
        pattern_err_msg="Email address verification failed.",
        request_only=True,
    )
    password: str = field(request_only=True)


@schema
class Token(APIResponse):
    auth_token: str = field(description="A JSON Web Token used for authentication.")
    token_type: str = field(default="Bearer")


class UserModel(Base, DBMixin):
    __tablename__ = "user"

    email = Column(String(255), unique=True, nullable=True)
    display_name = Column(String(255), unique=False, nullable=True)
    password = Column(String(255))
    admin = Column(Boolean, nullable=False, default=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)

    def __init__(self, email, display_name, password, admin=False):
        self.email = email
        self.display_name = display_name
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt(BCRYPT_LOG_ROUNDS)
        ).decode()
        self.admin = admin

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

import bcrypt
from molten import schema, field
from sqlalchemy import Column, String, Boolean

from ...db import Base, DBMixin

BCRYPT_LOG_ROUNDS = 11


@schema
class User:
    id: int = field(response_only=True)
    email: str
    display_name: str
    createdDate: str = field(response_only=True)
    modifiedDate: str = field(response_only=True)
    confirmed: bool = field(response_only=True)


class UserModel(Base, DBMixin):
    __tablename__ = 'user'

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

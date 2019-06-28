from typing import Optional
from molten import schema, field
from sqlalchemy import Column, Text, Boolean
from runcible.db import Base, DBMixin
from runcible import Link


@schema
class Todo:
    id: int = field(response_only=True)
    createdDate: str = field(response_only=True)
    modifiedDate: str = field(response_only=True)
    todo: str
    complete: Optional[bool]
    href: Link = field(response_only=True)


class TodoModel(Base, DBMixin):
    __tablename__ = "todo"
    todo = Column(Text)
    complete = Column(Boolean, default=False)

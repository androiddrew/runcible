from inspect import Parameter

from molten import BaseApp
from sqlalchemy.orm import Session

from runcible.manager import BaseManager
from runcible.error import EntityNotFound
from .model import User, UserModel


class UserManager(BaseManager):
    """A `UserManager` is  accountable for the CRUD operations associated with a `User` instance"""

    def schema_from_model(self, result: UserModel) -> User:
        _user = User(
            id=result.id,
            href=self.app.reverse_uri(
                "get_user_by_display_name", display_name=result.display_name
            ),
            createdDate=result.created_date,
            modifiedDate=result.modified_date,
            email=result.email,
            display_name=result.display_name,
            confirmed=result.confirmed,
            active=result.active,
            password=result.password,
        )
        return _user

    def model_from_schema(self, user: User) -> UserModel:
        _user_model = UserModel(
            email=user.email, display_name=user.display_name, password=user.password
        )
        return _user_model

    def get_user_by_display_name(self, display_name) -> User:
        """Retrieves a `User` representation by display_name."""
        result = (
            self.session.query(UserModel)
            .filter_by(display_name=display_name)
            .one_or_none()
        )
        if result is None:
            raise EntityNotFound(f"User: {display_name} does not exist")
        return self.schema_from_model(result)

    def create_user(self, user: User) -> User:
        """Creates a new `User` resource and returns its representation"""
        user_model = self.model_from_schema(user)
        self.session.add(user_model)
        self.session.flush()
        return self.schema_from_model(user_model)


class UserManagerComponent:
    is_cacheable = True
    is_singleton = False

    def can_handle_parameter(self, parameter: Parameter) -> bool:
        return parameter.annotation is UserManager

    def resolve(self, session: Session, app: BaseApp) -> UserManager:  # type: ignore
        return UserManager(session, app)

from typing import List
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.repositories.main import AbstractRepository
from app.schemas.user import User, CreateUser, UpdateUser
from app.schemas.auth import UserCredentials


class UserRepository(AbstractRepository[UserModel]):
    """
    Repository class for handling CRUD operations related to User entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the UserRepository with a database session.
        """
        super().__init__(db)
        self.model = UserModel

    def create_user(self, user: CreateUser) -> User:
        """
        Create a new user.
        """
        try:
            entity = UserModel(
                name=user.name,
                username=user.username,
                password=user.password
            )
            return self._create(entity)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by its ID.
        """
        try:
            return self._get(user_id)
        except Exception as e:
            raise e

    def update_user(self, user: UpdateUser) -> User:
        """
        Update a user.
        """
        try:
            return self._update(user)
        except Exception as e:
            self._db.rollback()
            raise e

    def delete_user_by_id(self, user_id: int) -> None:
        """
        Delete a user by its ID.
        """
        try:
            self._delete(user_id)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_all_users(self) -> List[User]:
        """
        Retrieve all users.
        """
        try:
            return self._get_all()
        except Exception as e:
            raise e

    def get_user_by_username(self, value: str) -> User:
        """
       Retrieve a user by its username.
        """
        try:
            return self._search_one_with("username", value)
        except Exception as e:
            raise e

    def get_user_credentials(self, username: str) -> UserCredentials:
        """
        Retrieve user credentials by username.
        """
        try:
            return self._search_one_with("username", username)
        except Exception as e:
            raise e

from fastapi import HTTPException, Response
from typing import List

from app.config.session import AppService
from app.schemas.user import User, CreateUser, UpdateUser
from app.schemas.auth import UserCredentials
from app.repositories.user import UserRepository
from app.utils.hash import Hash

class UserService(AppService):
    """
    Service layer for managing user operations.

    Attributes:
        db (Session): Database session object.

    """

    def create_user(self, user: CreateUser) -> User:
        """
        Creates a new user.

        Args:
            user (CreateUser): User data including username and password.

        Returns:
            User: Created user object.

        Raises:
            HTTPException: If the username already exists.
        """
        user_data = UserRepository(self.db).get_user_by_username(user.username)

        if user_data:
            raise HTTPException(status_code=409, detail="Username already exists")

        user.password = Hash.hash(user.password)
        
        return UserRepository(self.db).create_user(user)

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by ID.

        Args:
            user_id (int): ID of the user.

        Returns:
            User: Retrieved user object.

        Raises:
            HTTPException: If the user with the specified ID is not found.
        """
        user_data = UserRepository(self.db).get_user_by_id(user_id)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        return user_data

    def update_user_by_id(self, user_id: int, user: UpdateUser) -> User:
        """
        Updates a user's details.

        Args:
            user_id (int): ID of the user to update.
            user (UpdateUser): Updated user data.

        Returns:
            User: Updated user object.

        Raises:
            HTTPException: If the username is already taken by another user.
                           If the user with the specified ID is not found.
        """
        user_data = self.get_user_by_id(user_id)
        
        if user_data.username != user.username:
            existing_user = UserRepository(self.db).get_user_by_username(user.username)
            
            if existing_user:
                raise HTTPException(status_code=409, detail="Username already exists")

        return UserRepository(self.db).update_user(user)

    def delete_user_by_id(self, user_id: int) -> Response:
        """
        Deletes a user by ID.

        Args:
            user_id (int): ID of the user to delete.

        Returns:
            Response: HTTP response indicating success (status code 204) or failure.

        Raises:
            HTTPException: If the user with the specified ID cannot be deleted.
        """
        user_data = self.get_user_by_id(user_id)
        
        UserRepository(self.db).delete_user(user_data.id)
        
        existing_user = UserRepository(self.db).get_user_by_id(user_id)
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Can't delete user")
        
        return Response(status_code=204)

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users.

        Returns:
            List[User]: List of all user objects.
        """
        return UserRepository(self.db).get_all_users()
    
    def get_user_by_username(self, value: str) -> User:
        """
        Retrieves a user by username.

        Args:
            value (str): Username of the user to retrieve.

        Returns:
            User: Retrieved user object.
        """
        return UserRepository(self.db).get_user_by_username(value)
    
    def get_user_credentials(self, username: str) -> UserCredentials:
        """
        Retrieves user credentials (username and ID).

        Args:
            username (str): Username of the user.

        Returns:
            UserCredentials: User credentials object.
        """
        return UserRepository(self.db).get_user_credentials(username)

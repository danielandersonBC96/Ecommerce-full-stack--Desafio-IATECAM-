from fastapi import HTTPException, Response
from typing import List

from Config.session import Session
from Schemas.SchemaUser import User, CreateUser, UpdateUser
from Schemas.SchemaAuth import UserCredentials
from Repositories.RepositoriesUser import UserRepository
from Utils.Utils_Hash import Hash

class UserService:
    """
    Service layer for managing user operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: CreateUser) -> User:
        """
        Creates a new user.

        Args:
            user_data (CreateUser): User data including username and password.

        Returns:
            User: Created user object.

        Raises:
            HTTPException: If the username already exists.
        """
        existing_user = self.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(status_code=409, detail="Username already exists")

        hashed_password = Hash.hash(user_data.password)
        user_data_dict = user_data.dict()
        user_data_dict['password'] = hashed_password

        return UserRepository(self.db).create_user(user_data_dict)

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
        user_data = UserRepository(self.db).get_user_by_id(user_id)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user_data.username != user.username:
            existing_user = self.get_user_by_username(user.username)
            
            if existing_user:
                raise HTTPException(status_code=409, detail="Username already exists")

        return UserRepository(self.db).update_user(user_id, user.dict())

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
        user_data = UserRepository(self.db).get_user_by_id(user_id)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        UserRepository(self.db).delete_user(user_id)
        
        user_data = UserRepository(self.db).get_user_by_id(user_id)
        
        if user_data:
            raise HTTPException(status_code=400, detail="Can't delete user")
        
        return Response(status_code=204)

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users.

        Returns:
            List[User]: List of all user objects.
        """
        return UserRepository(self.db).get_all_users()

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

    def get_user_by_username(self, username: str) -> User:
        """
        Retrieves a user by username.

        Args:
            username (str): Username of the user to retrieve.

        Returns:
            User: Retrieved user object.
        """
        return UserRepository(self.db).get_user_by_username(username)
    
    def get_user_credentials(self, username: str) -> UserCredentials:
        """
        Retrieves user credentials (username and ID).

        Args:
            username (str): Username of the user.

        Returns:
            UserCredentials: User credentials object.
        """
        return UserRepository(self.db).get_user_credentials(username)
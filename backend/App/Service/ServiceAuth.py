from fastapi import HTTPException
from app.services.user import UserService
from app.schemas.user import CreateUser
from app.schemas.auth import RegisterUser, LoginUser
from app.utils.hash import Hash
from app.utils.jwt import JWTManager
from app.config.session import AppService

class AuthService(AppService):
    def register_user(self, user: RegisterUser) -> CreateUser:
        """
        Registers a new user in the system.

        Args:
            user (RegisterUser): User data for registration.

        Returns:
            CreateUser: Information of the created user.
        """
        user_data = CreateUser(
            name=user.name,
            username=user.username,
            password=user.password
        )
        return UserService(self.db).create_user(user_data)
    
    def login_user(self, user: LoginUser) -> dict:
        """
        Authenticates an existing user.

        Args:
            user (LoginUser): User data for login.

        Returns:
            dict: Access token generated upon successful authentication.
        
        Raises:
            HTTPException: If user credentials are invalid.
        """
        user_data = UserService(self.db).get_user_credentials(user.username)

        if not user_data:
            raise HTTPException(status_code=400, detail="User not found")
        
        equal_passwords = Hash.compare_hash(user.password, user_data.password)
        
        if not equal_passwords:
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        data = {
            "sub": user_data.username,
            "user_id": user_data.id
        }

        access_token = JWTManager().create_token(data)

        return { "access_token": access_token, "token_type": "bearer" }

from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import Optional

from app.config.config import get_settings

class JWTManager:
    def __init__(self):
        self.secret_key = get_settings().SECRET_KEY
        self.algorithm = get_settings().ALGORITHM
        self.token_expire_minutes = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES

    def create_token(self, data: dict) -> str:
        """
        Creates a new JWT token.

        Args:
            data (dict): Payload data to be encoded into the token.

        Returns:
            str: Encoded JWT token.

        Raises:
            HTTPException: If encoding the token fails.
        """
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)
            to_encode.update({"exp": expire})
            token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to create token")

    def decode_token(self, token: str) -> Optional[dict]:
        """
        Decodes a JWT token.

        Args:
            token (str): JWT token to decode.

        Returns:
            dict: Decoded payload if successful.

        Raises:
            HTTPException: If decoding the token fails or if the token is invalid/expired.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not decode token")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to decode token")

    def verify_token(self, token: str) -> bool:
        """
        Verifies if a JWT token is valid.

        Args:
            token (str): JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            payload = self.decode_token(token)
            return True
        except HTTPException:
            return False

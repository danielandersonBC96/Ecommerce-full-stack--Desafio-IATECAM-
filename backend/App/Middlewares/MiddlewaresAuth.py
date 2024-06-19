from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import JWTManager

# Instantiating the OAuth2PasswordBearer scheme once
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Instantiating the JWTManager once
jwt_manager = JWTManager()

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Function to retrieve the user payload from the JWT token.

    Args:
        token (str): JWT token received from the Authorization header.

    Returns:
        dict: Decoded payload from the JWT token.
    """
    try:
        # Verifying the token
        if not jwt_manager.verify_token(token):
            raise HTTPException(status_code=401, detail="Unauthorized token")

        # Decoding the token
        payload = jwt_manager.decode_token(token)

        return payload

    except JWTVerificationError as e:
        raise HTTPException(status_code=401, detail=f"Error verifying token: {str(e)}")

    except JWTDecodeError as e:
        raise HTTPException(status_code=401, detail=f"Error decoding token: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

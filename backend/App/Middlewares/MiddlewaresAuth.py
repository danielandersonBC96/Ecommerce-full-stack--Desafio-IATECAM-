from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import JWTManager

# Instanciando o esquema OAuth2PasswordBearer uma vez
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    jwt_manager = JWTManager()
    
    # Verificando o token
    if not jwt_manager.verify_token(token):
        raise HTTPException(status_code=401, detail="Token não autorizado")
    
    # Decodificando o token
    payload = jwt_manager.decode_token(token)
    
    return payload

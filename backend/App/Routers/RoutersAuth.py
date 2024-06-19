from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from App.config.database import get_db
from App.Service.ServiceAuth import AuthService
from App.Schemas.SchemaAuth import LoginUser, RegisterUser
from app.Schemas.SchemaUser import User
from fastapi.security import OAuth2PasswordRequestForm

#Create a new router to group related to authentication
router = APIRouter()

#Intace of the authentication service to handle business logic
auth_service = AuthService()

#Endipoint for user authentication via POST/auth/login
@router.post("/login")
def login( form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    try:
        # Create a LoginUser object base on the data received in the form 
        user_data = LoginUser(username=form_data.username, password=form_data,password)
        #Call the login_user methodo of AuthService to autenticate the user
        return auth_service.login_user(db,user_data)
    except Exception as e:
        # Handle generic expecption returnig an HTTP 500 with erro details 
        raise HTTPException( status_code=500, detail=str(e))

#Endpoint for registering a new user via POST/auth/register
@router.POST('/registe',response_model=User)
def register(user:RegisterUser, db:Session = Depends(get_db))

    try:
        #call the register_user method of AuthService to register a new user     
        return auth_service.register_user(db,user)
    except Exception as e:
        # handel generic expections returning an HTTP 500 with error details
        raise HTTPException(status_code,detail=str(e))
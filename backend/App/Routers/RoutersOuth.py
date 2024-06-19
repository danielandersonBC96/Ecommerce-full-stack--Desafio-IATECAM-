from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.services.output import OutputService
from app.schemas.output import Output, CreateOutput
from app.middlewares.auth import get_current_user

# Crate a new APIRouter instace for outputs

router = APIRouter(
    prefix="/outputs",  # Base path for all endpoints in this router
    tags=["Outputs"]    # Tag to group endpoints under in OpenAPI documentation

)

#Instance of OutputService class to handle output related logic 
output_service = OutputService()
#Endpoint to create a new output recorde

@router.post("/",response_model=Output)
def create_output(   output_data:CreateOutput ,db:Session = Depends(get_db),current_user: dist =Depends(get_current_user)):
    try:
        # call thr create_putput method of OutpService to create a new output record
        return output_service.create_output(current_user["user_id"], output_data)
    except Exception as e:
         # Handle exceptions by raising an HTTP 500 error with details
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to fetch the latest output records (sales)
@router.get("/latest-sales", response_model=List[Output])
def get_last_sells( db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    try:
         # Call the get_last_sells method of OutputService to fetch the latest output records
         return output_service.get_last_sells()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


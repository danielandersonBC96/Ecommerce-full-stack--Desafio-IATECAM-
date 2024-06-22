from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config.database import get_db
from Service.ServiceOutPut import OutputService  # Verifique o nome correto do módulo e da classe
from  Schemas.SchemaOutPut import Output, CreateOutput
from Middlewares.MiddlewaresAuth import get_current_user
from typing import List

router = APIRouter(
    prefix="/outputs",
    tags=["Outputs"]
)

@router.post("/", response_model=Output)
def create_output(
    output_data: CreateOutput,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        output_service = OutputService(db)  # Inicializa OutputService com a sessão do banco de dados
        return output_service.create_output(current_user["user_id"], output_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest-sales", response_model=List[Output])
def get_last_sells(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        output_service = OutputService(db)  # Inicializa OutputService com a sessão do banco de dados
        return output_service.get_last_sells()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

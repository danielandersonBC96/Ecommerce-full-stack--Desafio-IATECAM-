from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from Config.database import get_db

from Service.ServiceTag import TagService
from Schemas.SchemaTag import Tag, CreateTag  # Ajuste na importação de CreateTag
from Middlewares.MiddlewaresAuth import get_current_user
from Routers.sse import sse_manager

router = APIRouter(
    prefix="/tags",
    tags=["tag"]
)

@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: CreateTag, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
) -> Tag:
    """
    Create a new tag.
    """
    try:
        tag_data = TagService(db).create_tag(tag=tag)
        
        event_data = "tag_created"
        sse_manager.register_event_data(event_data)
        sse_manager.send_event(event_data)
        
        return tag_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Tag])
def get_all_tags(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
) -> List[Tag]:
    """
    Retrieve all tags.
    """
    try:
        return TagService(db).get_all_tags()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

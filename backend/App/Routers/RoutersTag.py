from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.services.tag import TagService
from app.schemas.tag import Tag, CreateTag
from app.middlewares.auth import get_current_user
from app.routers.sse import sse_manager

#Intace of the Tag  service to handle business logic
router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


#Create endpointe for creating a new tag.
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

#Create endpoint for retrieve a all tags 
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


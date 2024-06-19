from sqlalchemy.orm import Session, joinedload
from app.models.storage import Storage as StorageModel
from app.repositories.main import AbstractRepository
from app.schemas.storage import Storage, CreateStorage, UpdateStorage, StorageBase

from typing import List
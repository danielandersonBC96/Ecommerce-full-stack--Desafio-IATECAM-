from typing import TypeVar, Generic, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

ModelType = TypeVar("ModelType", bound=object)

class AbstractRepository(Generic[ModelType]):
    """
    Generic repository class for handling CRUD operations for SQLAlchemy models.

    """

    def __init__(self, db: Session):
        self.db = db

    def _create(self, entity: ModelType) -> ModelType:
        """
        Create a new entity in the database.

        """
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def _get(self, id: int) -> ModelType:
        """
        Retrieve an entity by its ID.
        """
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            raise e

    def _delete(self, id: int) -> None:
        """
        Delete an entity by its ID.
        """
        try:
            entity = self._get(id)
            if entity:
                self.db.delete(entity)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def _get_all(self) -> List[ModelType]:
        """
        Retrieve all entities of the specified model.

        """
        try:
            return self.db.query(self.model).all()
        except Exception as e:
            raise e

    def _search_all_without(self, field_name: str, value: str) -> List[ModelType]:
        """
        Search for entities where a specific field does not match a given value.

        """
        try:
            return self.db.query(self.model).filter(getattr(self.model, field_name) != value).all()
        except Exception as e:
            raise e

    def _search_all_with(self, field_name: str, value: str) -> List[ModelType]:
        """
        Search for entities where a specific field matches a given value.

        """
        try:
            return self.db.query(self.model).filter(getattr(self.model, field_name) == value).all()
        except Exception as e:
            raise e

    def _search_one_with(self, field_name: str, value: str) -> ModelType:
        """
        Search for the first entity where a specific field matches a given value.

        """
        try:
            return self.db.query(self.model).filter(getattr(self.model, field_name) == value).first()
        except Exception as e:
            raise e

    def _get_last_n_records(self, field_name: str, n: int) -> List[ModelType]:
        """
        Retrieve the last N records ordered by a specified field.

        """
        try:
            return self.db.query(self.model).order_by(desc(getattr(self.model, field_name))).limit(n).all()
        except Exception as e:
            raise e

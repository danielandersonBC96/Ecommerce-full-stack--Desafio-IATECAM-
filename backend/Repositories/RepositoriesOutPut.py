from typing import List
from sqlalchemy.orm import Session
from Models.ModelsOutPut import Output as OutputModel
from Repositories.main import AbstractRepository
from Schemas.SchemaOutPut import Output, CreateOutput


class OutputRepository(AbstractRepository):
    """
    Repository class for handling CRUD operations related to Output entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the OutputRepository with a database session.

        """
        super().__init__(db)
        self.model = OutputModel

    def create_output(self, user_id: int, output: CreateOutput) -> Output:
        """
        Create a new Output record.

        """
        try:
            entity = OutputModel(
                user_id=user_id,
                storage_id=output.storage_id,
                amount=output.amount,
            )
            return self._create(entity)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_output_by_id(self, output_id: int) -> Output:
        """
        Retrieve an Output record by its ID.
.
        """
        try:
            return self._get(output_id)
        except Exception as e:
            raise e

    def delete_output_by_id(self, output_id: int) -> Output:
        """
        Delete an Output record by its ID.

        """
        try:
            return self._delete(output_id)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_all_outputs(self) -> List[Output]:
        """
        Retrieve all Output records.
        """
        try:
            return self._get_all()
        except Exception as e:
            raise e

    def get_outputs_by_user_id(self, user_id: int) -> List[Output]:
        """
        Retrieve all Output records associated with a user ID.

        """
        try:
            return self._search_all_with("user_id", user_id)
        except Exception as e:
            raise e

    def get_last_outputs(self, limit: int = 4) -> List[Output]:
        """
        Retrieve the last N Output records.

        """
        try:
            return self._get_last_n_records("created_at", limit)
        except Exception as e:
            raise e

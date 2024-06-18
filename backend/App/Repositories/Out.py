from sqlalchemy.orm import Session
from app.models.output import Output as OutputModel
from app.repositories.main import AbstractRepository
from app.schemas.output import Output, CreateOutput

from typing import List

class OutPutRepositoy(AbstractRepository[OutputModel]):
    def __init__(self, db: Session):
        super().__init__(db)
        self.models = OutputModel
    
    def create_output(self, user_id: int , output: CreateOutput) -> Output:
        entity = OutputModel(
             user_id=user_id,
            storage_id=output.storage_id,
            amount=output.amount,
        )
        return self._create(entity)

    def get_out_by_id( self, output_id:int) -> Output:
        return self._get(output_id)

    def delete_output_by_id(self, output: int) -> Output:
        return self._delete(output_id)
    
    def get_all_outputs(self) -> List[Output]:
        return self._get_all()
    
    def get_all_outputs_by_user_idd(self, user_id: int) -> List[Output]:
        return self._search_all_with("user_id", user_id)
        
     def get_last_outputs(self) -> List[Output]:
        return self._get_last_n_records("created_at", 4)
    
from fastapi import HTTPException, Response
from typing import List

from Schemas.SchemaOutPut import Output, CreateOutput
from Repositories.RepositoriesOutPut import OutputRepository
from Service.ServiceStorage import StorageService
from Service.ServiceTag import TagService
from Service.ServiceSalesProduct import SalesByProductService
from Config.session import AppService

class OutputService(AppService):
    """
    Service layer for managing outputs (sales) in the application.

    Handles creation, retrieval, deletion, and listing of outputs.

"""

    def create_output(self, user_id: int, output: CreateOutput) -> Output:
        """
        Creates a new output (sale) for a given user.

        """
        storage_data = StorageService(self.db).get_storage_by_id(output.storage_id)

        if storage_data.amount < output.amount:
            raise HTTPException(status_code=400, detail="Insufficient storage for this product")
        
        storage_data.amount -= output.amount

        SalesByTagService(self.db).add_to_analytics(storage_data.tag.id, output.amount)
        SalesByProductService(self.db).add_to_analytics(storage_data.product.id, output.amount)
        
        return OutputRepository(self.db).create_output(user_id, output)

    def get_output_by_id(self, output_id: int) -> Output:
        """
        Retrieves an output by its ID.

        """
        output_data = OutputRepository(self.db).get_output_by_id(output_id)
        
        if not output_data:
            raise HTTPException(status_code=404, detail="Output not found")

        return output_data

    def delete_output_by_id(self, output_id: int) -> Response:
        """
        Deletes an output by its ID.

        """
        output_data = self.get_output_by_id(output_id)
        
        OutputRepository(self.db).delete_output_by_id(output_data.id)
        
        # Check if the output was successfully deleted
        existing_output = OutputRepository(self.db).get_output_by_id(output_data.id)
        
        if existing_output:
            raise HTTPException(status_code=400, detail="Cannot delete output")
        
        return Response(status_code=204)

    def get_all_outputs(self) -> List[Output]:
        """
        Retrieves all outputs in the system.

        """
        return OutputRepository(self.db).get_all_outputs()
    
    def get_all_outputs_by_user_id(self, user_id: int) -> List[Output]:
        """
        Retrieves all outputs created by a specific user.

        """
        return OutputRepository(self.db).get_all_outputs_by_user_id(user_id)

    def get_last_sells(self) -> List[Output]:
        """
         Retrieves the latest outputs (sales).
        """
        return OutputRepository(self.db).get_last_outputs()

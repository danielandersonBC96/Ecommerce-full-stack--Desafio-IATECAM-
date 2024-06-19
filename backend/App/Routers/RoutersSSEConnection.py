from fastapi import FastAPI, APIRouter, HTTPException
from app.utils.sse import sse_manager

# Create a FastAPI application instance
app = FastAPI()

# Create an APIRouter instance to manage endpoints
router = APIRouter()

# Define a GET endpoint for SSE (Server-Sent Events)
@router.get("/api/sse")
async def sse_endpoint():
    """
    Endpoint to handle Server-Sent Events (SSE).

    Returns:
        An asynchronous response from sse_manager.sse_endpoint().
    """
    try:
        return await sse_manager.sse_endpoint()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Include the router in the FastAPI application
app.include_router(router)

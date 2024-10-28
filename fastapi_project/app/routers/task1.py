from fastapi import APIRouter
from ..config import logger

router = APIRouter()

@router.get("/task-1")
def example_endpoint():
    return {"message": "This is an task -1 example endpoint!"}

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    logger.info(f"Item endpoint called with item_id: {item_id}")
    if item_id <= 0:
        logger.error("Invalid item_id, must be greater than 0")
        return {"error": "Item ID must be greater than 0."}
    return {"item_id": item_id}
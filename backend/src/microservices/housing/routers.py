from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def housing_home():
    return {"detail": "housing Module Home Page"}

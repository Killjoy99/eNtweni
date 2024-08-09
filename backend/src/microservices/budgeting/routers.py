from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def budgeting_home():
    return {"detail": "Budgeting Module Home Page"}

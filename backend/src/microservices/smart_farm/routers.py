from fastapi import APIRouter

router = APIRouter()


@router.get("", name="smart_farm_home")
async def smart_farm_home():
    return {"detail": "Smart Farm Home"}

from fastapi import APIRouter

router = APIRouter()


@router.get("", name="shop_home")
async def shop_home():
    return {"detail": "Shop Home"}

from fastapi import APIRouter

router = APIRouter()


@router.get("", name="smsportal_home")
async def smsportal_home():
    return {"detail": "SMS Portal Home"}

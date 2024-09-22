from fastapi import APIRouter

router = APIRouter()


@router.get("", name="chat_home")
async def chat_home():
    return {"detail": "Chat Home"}

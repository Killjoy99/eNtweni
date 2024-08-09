from fastapi import APIRouter

router = APIRouter()


@router.get("", name="school_home")
async def school_home():
    return {"detail": "School Module Home Page"}

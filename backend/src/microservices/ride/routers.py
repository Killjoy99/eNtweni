from fastapi import APIRouter

router = APIRouter()


@router.get("", name="ride_home")
async def ride_home():
    return {"detail": "Ride Home"}

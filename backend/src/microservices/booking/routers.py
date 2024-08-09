from fastapi import APIRouter

router = APIRouter()


@router.get("", name="booking_home")
async def get_bookings():
    # Implementation
    return {"message": "Booking Module Home Page"}


@router.post("/bookings")
async def create_booking():
    # Implementation
    return {"message": "Booking created"}

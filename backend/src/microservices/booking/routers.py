from core.utils import templates
from fastapi import APIRouter, Request, Response, status

router = APIRouter()


@router.get("", name="booking_home")
async def bookings_index(request: Request, response: Response):
    # Implementation
    return templates.TemplateResponse(
        request=request,
        name="microservices/booking/index.html",
        status_code=status.HTTP_200_OK,
        context={},
    )


@router.post("/bookings")
async def create_booking():
    # Implementation
    return {"message": "Booking created"}

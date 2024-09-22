from typing import List, Optional

from pydantic import BaseModel, EmailStr

STRONG_PASSWORD_PATTERN = (
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


class UserRegistrationSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: Optional[List[int]] = []
    uploaded_image: Optional[str] = None

    # @field_validator("password")
    # def valid_password(cls, password: str) -> str:
    #     if not re.match(STRONG_PASSWORD_PATTERN, password):
    #         raise ValueError(
    #             "Password must contain at least 8 characters, "
    #             "one lowercase letter, one uppercase letter, "
    #             "one digit, and one special character"
    #         )
    #     return password

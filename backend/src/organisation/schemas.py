# from pydantic import BaseModel, EmailStr

# class OrganisationBase(BaseModel):
#     name: str
#     description: str | None = None
#     email: EmailStr | None = None
#     website: str | None = None

# class OrganisationCreate(OrganisationBase):
#     pass

# class OrganisationUpdate(OrganisationBase):
#     pass

# class OrganisationResponse(OrganisationBase):
#     id: int
#     creator_id: int

#     class Config:
#         from_attributes = True

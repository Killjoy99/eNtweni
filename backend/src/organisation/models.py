# from datetime import datetime, timezone

# from database.core import Base
# from pydantic import EmailStr
# from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship


# class Organisation(Base):
#     __tablename__ = "organisations"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String(length=150))
#     description: Mapped[str] = mapped_column(String(length=500))
#     creator_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("users.id"), nullable=False
#     )
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime, default=datetime.now(timezone.utc)
#     )
#     website: Mapped[str] = mapped_column(String, nullable=True)

#     # Relationships
#     creator = relationship("User", back_populates="organisations")
#     users = relationship(
#         "OrganisationUser", back_populates="organisation", cascade="all, delete-orphan"
#     )

#     def __repr__(self) -> str:
#         return f"Organisation(name={self.name}, creator_id={self.creator_id})"


# class OrganisationUser(Base):
#     __tablename__ = "organisation_users"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     organisation_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("organisations.id"), nullable=False
#     )
#     email: Mapped[EmailStr] = mapped_column(
#         String(length=128), unique=True, index=True, nullable=False
#     )
#     hashed_password: Mapped[str] = mapped_column(String(length=255), nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime, default=datetime.now(timezone.utc)
#     )

#     # Relationships
#     organisation = relationship("Organisation", back_populates="users")

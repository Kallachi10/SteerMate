"""Pydantic schemas for user profile."""

from pydantic import BaseModel, Field


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    name: str | None = Field(None, max_length=255)

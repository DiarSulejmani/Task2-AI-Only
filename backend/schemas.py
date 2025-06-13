"""backend/schemas.py

Pydantic models used by DuoQuanto backend – user-related schemas only for now.
We purposefully avoid the optional `email-validator` dependency to keep the
requirements lean for local development and automated evaluation.
"""
from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, constr

# Basic email pattern – does *not* guarantee full RFC compliance but good enough
# for demo & development without heavy dependencies.
EmailStr = constr(pattern=r"[^@]+@[^@]+\.[^@]+", min_length=3, max_length=320)


class UserBase(BaseModel):
    full_name: constr(strip_whitespace=True, min_length=1, max_length=255)
    email: EmailStr  # type: ignore[valid-type]


class UserCreate(UserBase):
    password: constr(min_length=6, max_length=128)
    role: constr(strip_whitespace=True) = "student"


class UserLogin(BaseModel):
    email: EmailStr  # type: ignore[valid-type]
    password: constr(min_length=6, max_length=128)


class UserOut(UserBase):
    id: int
    role: str
    created_at: dt.datetime

    class Config:
        orm_mode = True


status = "ok"
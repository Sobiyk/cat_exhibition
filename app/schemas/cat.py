from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.breed import CatBreedDB


class CatBase(BaseModel):
    name: str
    color: str
    age: int
    description: str


class CatCreate(CatBase):
    breed: str


class CatUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None
    breed: Optional[str] = None


class CatDB(CatBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    breed: CatBreedDB

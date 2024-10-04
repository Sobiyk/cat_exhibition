from pydantic import BaseModel, ConfigDict


class CatBreedDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class BreedDB(CatBreedDB):
    id: int

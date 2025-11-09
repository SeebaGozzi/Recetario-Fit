
from typing import List, Optional
from pydantic import BaseModel

class RecipeCreate(BaseModel):
    title: str
    category: Optional[str] = None
    ingredients: List[str]
    steps: str
    is_healthy: Optional[bool] = True

class RecipeOut(RecipeCreate):
    id: int
    class Config:
        orm_mode = True

class PDFOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    filename: str
    class Config:
        orm_mode = True

class PDFOutMeta(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    filename: str

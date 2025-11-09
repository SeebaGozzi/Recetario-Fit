
from sqlalchemy import Column, Integer, String, Boolean, Text, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON as JSONType
from .database import Base

try:
    JSONTypeDB = JSONB
except Exception:
    JSONTypeDB = JSONType

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True)
    ingredients = Column(JSONTypeDB, nullable=False)  # list[str]
    steps = Column(Text, nullable=False)
    is_healthy = Column(Boolean, default=True)

class RecipePDF(Base):
    __tablename__ = "recipe_pdfs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False, default="application/pdf")
    data = Column(LargeBinary, nullable=False)

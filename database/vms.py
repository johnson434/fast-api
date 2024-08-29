from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, JSON

class VM(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str | None = None
    description: str = "기본 설명"
    
class VMInsert(SQLModel):
    title: str
    image: str | None = None
    description: str = "기본 설명"
    
class VMUpdate(SQLModel):
    title: str
    image: str | None = None
    description: str = f"{id}"
from typing import Optional
from pydantic import BaseModel, Field
import uuid

class Task(BaseModel):
    description: Optional[str] = Field(None, title="Description of a task") # Opcional, vem como default None
    status: Optional[bool] = Field(None, title="current task status") # Opcional, vem como default None

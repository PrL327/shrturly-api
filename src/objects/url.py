from pydantic import BaseModel

class URL(BaseModel):
    code: str
    path: str    
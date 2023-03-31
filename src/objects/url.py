from pydantic import BaseModel;
import uuid
import datetime

class URL(BaseModel):
    code: str
    path: str
    uuid: str
    createdAt: datetime.datetime

    
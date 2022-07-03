from pydantic import BaseModel
from typing import List

class URLBase(BaseModel):
    original_url: str

class URL(URLBase):
    clicks: int

    class Config:
        orm_mode = True

class URLInfo(URL):
    short_url: str

class URLListResponse(BaseModel):
    __root__ : List[URLInfo]

class CreateURLResponse(BaseModel):
    url : str

from typing import Optional, Union
from pydantic import BaseModel, Field, validator


class Hset(BaseModel):
    key: str
    field: str
    val: Union[str, int, float, bytes] = ''
    mapping: Optional[dict] = None
    ttl: Optional[int] = Field(0, ge=0)
    
    
class Hmset(BaseModel):
    key: str
    mapping: dict
    ttl: Optional[int] = Field(0, ge=0)

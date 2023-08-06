from typing import Optional, Union
from pydantic import BaseModel, Field, validator


ttl = 1209600    # seconds


class StarterModel(BaseModel):
    key: str
    pre: Optional[Union[str, int, float]] = ''
    ver: Optional[Union[str, int, float]] = ''
    ttl: Optional[int] = Field(ttl, ge=0)


class Hset(StarterModel):
    field: str
    val: Union[str, int, float, bytes] = ''
    mapping: Optional[dict] = None
    
    
class Hmset(StarterModel):
    mapping: dict

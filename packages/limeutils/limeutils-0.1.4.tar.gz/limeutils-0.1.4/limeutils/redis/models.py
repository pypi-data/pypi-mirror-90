from typing import Optional, Union
from pydantic import BaseModel, Field, validator



class StarterModel(BaseModel):
    key: str
    pre: Optional[Union[str, int, float]] = ''
    ver: Optional[Union[str, int, float]] = ''
    ttl: Optional[int] = Field(0, ge=0)


class Hset(StarterModel):
    field: str
    val: Union[str, int, float, bytes] = ''
    mapping: Optional[dict] = None
    
    
class Hmset(StarterModel):
    mapping: Optional[dict] = None


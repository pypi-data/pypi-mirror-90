from typing import Optional, Union, TypeVar
from pydantic import BaseModel, Field, validator


LT = Union[list, tuple]
V = Union[str, int, float, bytes]



def listmaker(val):
    if isinstance(val, str):
        return [val]
    return val


class StarterModel(BaseModel):
    key: V
    pre: Optional[V] = ''
    ver: Optional[V] = ''
    ttl: Optional[int] = Field(0, ge=0)


class Hset(StarterModel):
    field: str
    val: Optional[V]
    mapping: Optional[dict] = None
    
    @validator('val')
    def nonone(cls, val):
        if val is None:
            return ''
        return val
    
    
class Hmset(StarterModel):
    mapping: Optional[dict] = None

    @validator('mapping')
    def nonone(cls, val):
        for k, v in val.items():
            if v is None:
                val[k] = ''
        return val
    
    
class Hmget(StarterModel):
    fields_: Optional[LT] = None


class Hdel(StarterModel):
    fields_: Optional[Union[str, LT]] = None
    
    @validator('fields_')
    def makelist(cls, val):
        return listmaker(val)
    
    
class Delete(BaseModel):
    key: Union[str, LT]
    pre: Optional[V] = ''
    ver: Optional[V] = ''

    @validator('key')
    def makelist(cls, val):
        return listmaker(val)
from typing import Optional, Union, Any
from pydantic import BaseModel, Field, validator


LT = Union[list, tuple]
V = Union[str, int, float, bytes]



def listmaker(val):
    """Validator: Convert str to list with one item."""
    if isinstance(val, str):
        return [val]
    return val

def nonone(val):
    """Validator: Convert None to empty string."""
    if val is None:
        return ''
    return val

def nonone_mapping(val):
    """Validator: Convert None to empty string."""
    if val is None or not val:
        return None
    else:
        for k, v in val.items():
            val[k] = '' if v is None else v
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

    _clean_val = validator('val', allow_reuse=True)(nonone)
    _clean_mapping = validator('mapping', allow_reuse=True)(nonone_mapping)
    
    
class Hmset(StarterModel):
    mapping: Optional[dict] = None
    
    _clean_mapping = validator('mapping', allow_reuse=True)(nonone_mapping)


class Set(StarterModel):
    val: Optional[V] = ''
    xx: bool = False
    keepttl: bool = False

    _clean_val = validator('val', allow_reuse=True)(nonone)

    
    @validator('xx', 'keepttl')
    def boolonly(cls, val):
        return bool(val)
    

class Get(StarterModel):
    default: Optional[Any] = ''


class Hget(StarterModel):
    default: Optional[Any] = ''

    
class Hmget(StarterModel):
    fields_: Optional[LT] = None


class Hdel(StarterModel):
    fields_: Optional[Union[str, LT]] = None
    
    _clean_fields = validator('fields_', allow_reuse=True)(listmaker)
    
    
class Delete(BaseModel):
    key: Union[str, LT]
    pre: Optional[V] = ''
    ver: Optional[V] = ''

    _clean_fields = validator('key', allow_reuse=True)(listmaker)


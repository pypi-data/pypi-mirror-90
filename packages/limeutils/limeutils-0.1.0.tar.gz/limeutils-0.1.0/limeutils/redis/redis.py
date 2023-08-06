import redis as reds
from typing import Optional, Union, Any

from . import models
from limeutils import byte_conv, parse_str
# from app.settings import settings as s



class RedisUtil:
    cookie_ttl = 1209600    # seconds
    prefix = ''
    
    def __init__(self, **kwargs):
        self.r = reds.Redis(**kwargs)
        

    # def hset(self, key: str, field: str, val: Union[str, int, float, bytes],
    #          ttl: int, mapping: dict) -> bool:
    def hset(self, key: str, field: str, val: Union[str, int, float, bytes] = '',
             mapping: Optional[dict] = None, ttl: Optional[int] = 0):
        """
        Add a single hash key using HSET
        :param key:     Hash key name
        :param field:   Field in the key
        :param val:     Value
        :param mapping: More data(?)
        :param ttl:     ttl
        :return:        bool
        """
        data = models.Hset(key=key, field=field, val=val, mapping=mapping, ttl=ttl)
        ttl = data.ttl and data.ttl or self.cookie_ttl
        prefix = self.prefix
        
        if prefix:
            data.key = f'{prefix}:{data.key}'

        self.r.hset(data.key, data.field, data.val, data.mapping)
        self.r.expire(data.key, ttl)
        return True
        


    def hmset(self, *, key: str, mapping: dict, ttl: Optional[int] = 0) -> bool:
        """
        Add a single hash key using HSET. An alias for hset since hmset is deprecated.
        :param key:     Hash key name
        :param mapping: Fields in the key
        :param ttl:     ttl
        :return:        bool
        """
        data = models.Hmset(key=key, mapping=mapping, ttl=ttl)
        data.ttl = data.ttl and data.ttl or self.cookie_ttl
        prefix = self.prefix

        if prefix:
            data.key = f'{prefix}:{data.key}'
        
        for k, v in data.mapping.items():
            if v is None:
                data.mapping[k] = ''
        # mapping = {k: v is None and '' or v for k, v in mapping.items()}

        self.r.hmset(data.key, mapping=data.mapping)
        self.r.expire(data.key, data.ttl)
        return True


# def hget(key: str, field: str, default='') -> (int, float, str):         # noqa
#     """
#     Get a single hash value from redis using HGET
#     :param key:    Name
#     :param field:     Key
#     :param default: Default if !key
#     :return:        int, float, str, or None
#     """
#     if not isinstance(field, str):
#         raise TypeError("Key must be a string since you're only getting one value. For multiple "
#                         "values use hmget.")
#
#     prefix = get_cache_prefix()
#     key = f'{prefix}:{key}'
#
#     val = redis.hget(key, field)
#     val = byte_conv(val)
#     return val != 'n' and val or default
#
#
# def hmget(key: str, fields: Optional[Union[list, tuple]] = None) -> dict:
#     """
#     Get multiple hash values form redis using HMGET
#     :param key:    Name
#     :param fields:    A list of keys or leave empty to return all keys in that name
#     :return:        A dict with all values parsed to either int, float, str, or None
#     """
#     # if keys:
#     #     if not isinstance(keys, (list, tuple)):
#     #         raise TypeError("Keys must be a list or tuple since you're getting multiple values. For "
#     #                         "single values use hget.")
#
#     prefix = get_cache_prefix()
#     key = f'{prefix}:{key}'
#
#     if fields:
#         val_list = redis.hmget(key, fields)
#         val_list = map(lambda x: x is not None and byte_conv(x) or x, val_list)
#         val_dict = dict(zip(fields, val_list))
#     else:
#         val_dict = redis.hgetall(key)
#         k = map(lambda x: x is not None and byte_conv(x) or x, val_dict.keys())
#         v = map(lambda x: x is not None and byte_conv(x) or x, val_dict.values())
#         val_dict = dict(zip(k, v))
#     return val_dict
#
#
# def hdel(key: str, *fields) -> int:
#     """
#     Delete a field from a a hash key
#     Args:
#         key (str): Key name with prefixes, if any
#         *fields (str): Field names
#
#     Returns:
#         Number of items deleted
#     """
#     prefix = get_cache_prefix()
#     key = f'{prefix}:{key}'
#
#     count = redis.hdel(key, *fields)
#
#     return count
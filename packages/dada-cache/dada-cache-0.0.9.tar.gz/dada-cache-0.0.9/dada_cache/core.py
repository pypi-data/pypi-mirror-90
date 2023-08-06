"""
An abstract Redis cache. TODO: abstract out into separate library + add file/s3 caching.
"""


import logging
import pickle
from hashlib import md5
from typing import Any, Dict
from datetime import datetime

from dada_types import T
from dada_types.base import SerializableObject
from dada_utils import dates, etc
import dada_serde

CACHE_LOGGER = logging.getLogger()


class CacheResponse(SerializableObject):
    __module__ = "dada_cache.core"
    __dada_type__ = "cache_response"

    """
    A class that we return from a cache request.
    """

    def __init__(
        self,
        key: T.text.py,
        value: Any,
        expiration: int,
        updated_at: T.date_tz.py_optional,
        is_cached: T.bool.py,
        debug: T.bool.py,
        *args,
        **kwargs,
    ):
        self.key = key
        self.value = value
        self.expiration = expiration
        self.updated_at = updated_at
        self.is_cached = is_cached
        self.debug = debug
        self.args = args
        self.kwargs = kwargs

    @property
    def age(self) -> T.seconds.py:
        if self.is_cached:
            return (dates.now() - self.updated_at).seconds
        return 0

    @property
    def display_age(self) -> T.text.py:
        """"""
        return T.seconds.hum(self.age)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the cache response as a dict
        """
        return etc.AttrDict(
            {
                "key": self.key,
                "args": self.args,
                "kwargs": self.kwargs,
                "expiration": self.expiration,
                "age": self.age,
                "value": self.value,
                "display_age": self.age,
                "updated_at": self.updated_at,
                "is_cached": self.is_cached,
                "debug": self.debug,
            }
        )

    def get_value(self) -> Any:
        """
        Get the value of the cache response.
        """
        return self.value


class BaseCache(SerializableObject):
    """
    An abstract cache to inherit from.
    """

    __module__ = "dada_cache"
    __dada_type__ = "cache"

    expiration = 84600  # 1 day
    key_prefix = "cache"
    key_sep = ":"
    key_suffix = ""
    debug = False
    defaults = {}

    def __init__(
        self,
        key_prefix: str = None,
        key_sep: str = ":",
        key_suffix: str = "",
        expiration: int = 84600,
        debug=False,
        **kwargs,
    ):

        self.key_prefix = key_prefix or self.key_prefix or self.object_name
        self.key_sep = key_sep or self.key_sep
        self.key_suffix = key_suffix or self.key_suffix
        self.expiration = expiration or self.expiration
        self.debug = self.debug or debug
        self.defaults.update(kwargs)

    # ////////////////////////////////////////////////
    # Format the cache key from the function signature
    # ////////////////////////////////////////////////

    def _format_key(self, *args, **kw) -> str:
        """
        Format a unique key for the cache based on the fetch function's parameters
        """
        # update kwargs with defaults
        kw = dict(list(self.defaults.items()) + list(kw.items()))

        # add args + kw to hash keys
        hash_keys = []
        for a in sorted(args):
            hash_keys.append(str(a))

        for k, v in sorted(kw.items()):
            hash_keys.append(str(k) + self.key_sep + str(v))

        # format the key by hashing the args + kwargs and apply key configurations
        func_sig = "".join([k for k in hash_keys if k])
        func_hash = md5(func_sig.encode("utf-8")).hexdigest()
        return self.key_prefix + self.key_sep + func_hash + self.key_suffix

    def format_key(self, *args, **kw) -> str:
        """
        Formatting the fx like this allows us
        to modify it's behavior.
        """
        return self._format_key(*args, **kw)

    # ////////////////////////////////////////////////
    # Methods to Implement/Overridde
    # ////////////////////////////////////////////////

    def get_age(self, *args, **kw) -> T.date_tz.py:
        """
        The function for checkout how old something is in the cache
        """
        raise NotImplementedError

    def set_age(self, age, expiration, *args, **kw) -> None:
        """
        The function for setting the age of something in the cache.
        """
        raise NotImplementedError

    def get_obj(self, *args, **kw):
        """
        The function for getting stuff from the cache
        """
        raise NotImplementedError

    def set_obj(self, obj, expiration, *args, **kw):
        """
        The function for putting stuff into the cache
        """
        raise NotImplementedError

    def rm(self, *args, **kw):
        """
        The function for removing stuff from the cache
        """
        raise NotImplementedError

    def ls(self):
        """
        The function for listing all keys in the cache
        """
        raise NotImplementedError

    def exists(self, *args, **kw):
        """
        The function for checking whether something exists in the cache
        """
        raise NotImplementedError

    def do(self, *args, **kw):
        """
        The function for doing the work we'd like to avoid repeating
        """
        raise NotImplementedError

    # ////////////////////////////////////////////////
    # Serialization protocol: Pickle by default, override for something else.
    # ////////////////////////////////////////////////

    def dump(self, o: Any, **kwargs) -> Any:
        """
        The function for deserializing the string
        returned from redis
        """
        return dada_serde.obj_to_pickle(o, **kwargs)

    def load(self, s: Any, **kwargs) -> Any:
        """
        The function for serializing the object
        returned from `get` to a string.
        """
        return dada_serde.pickle_to_obj(s, **kwargs)

    # ///////////// #
    # Invalidation  #
    # ///////////// #

    def invalidate_key(self, key: T.text.py) -> None:
        """
        Remove a key from the cache via raw key name
        """
        self.rm(key)

    def invalidate(self, *args, **kw) -> None:
        """
        Remove a key from the cache via it's function signaure
        """
        self.rm(self.format_key(*args, **kw))

    @classmethod
    def flush(cls) -> None:
        """
        Flush this cache.
        """
        for k in cls.ls():
            cls.rm(k)

    # ///////////////////////////
    # Core Get/Set Caching Logic
    # ///////////////////////////

    def _do(self, expiration, *args, **kw):
        """
        helper for wrapping the do exexcution
        """
        # TODO: error handling?
        obj = self.do(*args, **kw)

        # set the object in the cache at the specified key with the specified expiration
        self.set_obj(self.dump(obj), expiration, *args, **kw)

        # set the last modified time
        age = dates.now()
        self.set_age(age, expiration, *args, **kw)
        return obj, age

    def get(self, *args, **kw) -> CacheResponse:
        """
        The main get/cache function.
        """
        # combine keywords with defaults
        kw = dict(list(self.defaults.items()) + list(kw.items()))

        CACHE_LOGGER.debug(
            f"Fetching from cache {self.__dada_type__} using kwargs: {kw}"
        )

        # set vars
        expiration = kw.pop("expiration", self.expiration)
        key = self.format_key(*args, **kw)
        age = None
        obj = None
        is_cached = True

        # in debug mode we never cache
        if not self.debug:
            obj = self.get_obj(*args, **kw)
            if obj:
                obj = self.load(obj)
        # if it doesn't exist, proceed with work
        if not obj:
            is_cached = False
            obj, age = self._do(expiration, *args, **kw)

        # otherwise, proceed to fetching from cache
        else:
            # set metadata
            is_cached = True
            age = self.get_age(*args, **kw)

            # if it's too old procceed with work
            if (dates.now() - age).seconds > expiration:
                is_cached = False
                obj, age = self._do(expiration, *args, **kw)

            # otherwise deserialize the object
            else:
                obj = self.load(obj)

        # return the cache response
        return CacheResponse(key, obj, expiration, age, is_cached, self.debug)

    @property
    def expiration_human(self) -> T.text.py:
        """
        Get the expiration time in human-readable format
        """
        return T.seconds.hum(self.expiration)

    def to_dict(self) -> Dict[str, Any]:
        return etc.AttrDict(
            {
                "name": self.object_name,
                "info": self.object_info,
                "key_root": self.key_root,
                "key_prefix": self.key_prefix,
                "key_suffix": self.key_suffix,
                "key_sep": self.key_sep,
                "key_base": f"{self.key_root}:{self.key_prefix}",
                "expiration": self.expiration,
                "expiration_human": self.expiration_human,
            }
        )

import os
from datetime import datetime
from typing import Any

from dada_utils import path, dates
from dada_cache.core import BaseCache


class FileCache(BaseCache):

    cache_dir = os.path.expanduser("~/.dada/cache/")
    key_sep = "/"
    key_suffix = ".pkl"

    def format_key(self, *args, **kw):
        """
        Format a key for a file cache
        """
        return path.join(self.cache_dir, self._format_key(*args, **kw))

    def ensure_dir(self, *args, **kw):
        """
        Ensure a key directory exists in the file cache
        """
        return path.make_dir(path.get_dir(self.format_key(*args, **kw)))

    def get_age(self, *args, **kw) -> datetime:
        """
        Get the age of the object in the file cache.
        """
        return path.get_updated_at(self.format_key(*args, **kw))

    def set_age(self, age, expiration, *args, **kw) -> None:
        """
        Set the age of the object in the file cache.
        """
        return None  # NO-OP

    def rm(self, *args, **kw) -> None:
        """
        Remove a file from the local file cache.
        """
        return path.remove(self.format_key(*args, **kwargs))

    def ls(self):
        """
        List the files in the file cache
        """
        return path.list_files(self.cache_dir, ignore_hidden=True)

    def exists(self, *args, **kw) -> bool:
        """
        Check if an object iexists in a local file cache
        """
        return path.exists(self.format_key(*args, **kw))

    def get_obj(self, *args, **kw) -> Any:
        """
        Get the object from the file cache
        """
        with open(self.format_key(*args, **kw), "rb") as f:
            return f.read()

    def set_obj(self, obj, expiratiton, *args, **kw) -> None:
        """
        Set the object in the file cache
        """
        self.ensure_dir(*args, **kw)
        with open(self.format_key(*args, **kw), "wb") as f:
            f.write(obj)

    def flush(self):
        """
        Flush the file cache.
        """
        return path.remove(self.cache_dir)


class RedisCache(BaseCache):

    rdsconn = None

    def format_lm_key(self, *args, **kw) -> str:
        """
        Format the last modified date key for the redis cache
        """
        return f"{self.format_key(*args, **kw)}{self.key_sep}lm"

    def get_age(self, *args, **kw) -> datetime:
        """
        Get the age of the object in the redis cache
        """
        return dates.from_string(self.rdsconn.get(self.format_lm_key(*args, **kw)))

    def set_age(self, age, expiration, *args, **kw) -> None:
        """
        Set the age of the object in the redis cache
        """
        return self.rdsconn.set(
            self.format_lm_key(*args, **kw), age.isoformat(), ex=expiration
        )

    def get_obj(self, *args, **kw) -> Any:
        """
        Get the object from thee redis cache
        """
        return self.rdsconn.get(self.format_key(*args, **kw))

    def set_obj(self, obj, expiration, *args, **kw) -> None:
        """
        Put an object into the redis cache
        """
        return self.rdsconn.set(
            self.format_key(*args, **kw), self.dump(obj), ex=expiration
        )

    def rm(self, *args, **kw) -> None:
        """
        Remove an object from the redis cache
        """
        return self.rdsconn.delete(self.format_key(*args, **kw))

    def ls(self):
        """
        List the keys in the redis cache.
        """
        for key in self.rdsconn.keys():
            if key.startswith(self.key_prefix):
                yield key

    def exists(self, *args, **kw) -> bool:
        """
        Check if the object exists in the redis cache
        """
        return self.rdsconn.get(self.format_key(*args, **kw)) is not None


# TODO dada_store Cache


class DadaCache(BaseCache):

    dada_stor = None

import hashlib
import json
import sys
import time

from inspect import Parameter
from python_cli_generator import input_processor
from python_cli_generator.utils import decorator_factory

class CacheStorage():

    def __init__(self):
        self._mem_cache = {}

    def clean_cache(self):
        start_time = time.time()
        new_cache = {}
        for key in self._mem_cache:
            if (
                self._mem_cache[key]["expiration"] is not None
                and start_time - self._mem_cache[key]["time"] > self._mem_cache[key]["expiration"]
            ):
                pass
            else:
                new_cache[key] = self._mem_cache[key]
        
        self._mem_cache = new_cache

    def _get_hash(self, string_to_hash):
        return hash(string_to_hash)

    def get_cache(self, key):
        self.clean_cache()
        result = self._mem_cache.get(key,None)
        return result["response"] if result is not None else result

    def set_cache(self, key, result, expiration=30):
        if expiration < 0:
            expiration = None
        start_time = time.time()
        self._mem_cache[key] = {
            "response": result, 
            "time": start_time,  
            "expiration": expiration, 
        }

    def cache(self,expiration=30, key=None):
        def _cache_decorator(fn,*args, no_cache: bool = False, cache_salt: str = None, expiration = expiration, key=key,**kwargs):
            if key is None:
                key = self._get_hash(
                    json.dumps(
                        {
                            "args": list(args[1:]) + list(kwargs.values()),
                            "cache_salt": cache_salt,
                            "module": fn.__module__,
                            "func": fn.__name__,
                        },
                        default=lambda x: x.__dict__ if hasattr(x, '__dict__') else dir(x),
                        sort_keys=True,
                    )
                )
            cache_result = self.get_cache(key)
            if cache_result is not None and no_cache == False:
                return cache_result
            else:
                result = fn(*args, **kwargs)
                self.set_cache(key, result, expiration=expiration)
            return result

        no_cache = Parameter("no_cache", default=False,
                            kind=1, annotation=bool)

        return decorator_factory(call=_cache_decorator, custom_signature_parameters=[no_cache])
        


class CacheStorageFile(CacheStorage):

    def __init__(self,file_name = ".cache."+sys.argv[0].replace(".py","")):
        super().__init__()
        self.file_name = file_name
        self._mem_cache = None

    def _get_hash(self, string_to_hash):
        return hashlib.sha1(str.encode(string_to_hash)).hexdigest()

    def get_cache(self, key):
        self._mem_cache = input_processor.get_dict_from_file(self.file_name) if self._mem_cache is None else self._mem_cache
        return super().get_cache(key)
    
    def set_cache(self, key, result, expiration=30):
        super().set_cache(key, result, expiration)
        input_processor.set_file_from_dict(self.file_name, self._mem_cache)



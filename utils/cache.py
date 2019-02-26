import memcache
import config

cache = memcache.Client(config.MEMCACHED_PORT, debug=True)

def set(key, val, time=300):
    return cache.set(key=key, val=val, time=time)


def get(key):
    return cache.get(key=key)


def delete(key):
    return cache.delete(key=key)
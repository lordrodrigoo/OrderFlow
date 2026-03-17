from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


def reset_limiter():
    limiter._storage.reset()  # pylint: disable=protected-access

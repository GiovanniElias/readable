from __future__ import annotations

import os
import platform
import time


def timer(func):

    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        exc_time = end-start
        fn_name = func.__name__
        print(f'{fn_name} took {exc_time} to run.')
        return result

    return wrap

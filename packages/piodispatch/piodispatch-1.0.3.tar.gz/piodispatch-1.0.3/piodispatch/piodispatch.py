"""PioDispatch library's main module.
Copyright (c) Kiruse 2020. See license in LICENSE."""
from asyncio.futures import wrap_future
from concurrent.futures import ThreadPoolExecutor
from typing import Awaitable, Callable, TypeVar
import functools

pool = ThreadPoolExecutor(100, 'io-runner-')
T = TypeVar('T')

def ascoroutine(fn: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    @functools.wraps(fn)
    async def inner(*args, **kwargs):
        return await dispatch(fn, *args, **kwargs)
    return inner

def dispatch(callback: Callable[..., T], *args, **kwargs) -> Awaitable[T]:
    return wrap_future(pool.submit(callback, *args, **kwargs))

def shutdown():
    pool.shutdown()

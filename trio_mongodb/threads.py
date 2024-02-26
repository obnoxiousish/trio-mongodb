import trio

from functools import partial
from pymongo.collection import Collection

class AsyncCollectionWrapper:
    def __init__(self, collection: Collection):
        self.collection = collection

    async def _async_wrapper(self, method_name, *args, **kwargs):
        method = getattr(self.collection, method_name)
        executable = partial(method, *args, **kwargs)
        return await trio.to_thread.run_sync(executable)

    def __getattr__(self, name):
        async def method(*args, **kwargs):
            return await self._async_wrapper(name, *args, **kwargs)
        return method

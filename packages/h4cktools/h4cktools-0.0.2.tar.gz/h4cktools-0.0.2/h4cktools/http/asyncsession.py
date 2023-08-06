import asyncio
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import partial


__all__ = ["AsyncSession"]


class AsyncSession(requests.Session):
    """request.Session wrapper to make asynchronous requests
    """
    def __init__(self, loop=None, workers=4):
        super(AsyncSession, self).__init__()

        adapter = requests.adapters.HTTPAdapter(
            # The number of urllib3 connection pools to cache.
            pool_connections=workers,
            # The maximum number of connections to save in the pool 
            pool_maxsize=workers,
            # Block number of connections
            pool_block=True,
        )
        self.mount("http://", adapter)
        self.mount("https://", adapter)
        self.loop = loop or asyncio.get_event_loop()
        self.thread_pool = ThreadPoolExecutor(max_workers=workers)
        self.delay = 0


    def _request(self, *args, **kwargs):
        """Equivalent to requests.Session request method with delay
        """
        time.sleep(self.delay)
        return super(AsyncSession, self).request(*args, **kwargs)


    async def request(self, *args, **kwargs):
        """Send request to the concurrent executor.
        """
        func = partial(self._request, *args, **kwargs)
        return await self.loop.run_in_executor(self.thread_pool, func)


    def run(self, *coros) -> list:
        """Pass in all the coroutines you want to run.        
        It will wrap each one in a task, run it and wait for the result.

        Returns:
            list: Return a list with all results, 
                this is returned in the same order coros are passed in. 
        """
        completed, pending = self.loop.run_until_complete(asyncio.wait(coros))
        return [t.result() for t in completed]
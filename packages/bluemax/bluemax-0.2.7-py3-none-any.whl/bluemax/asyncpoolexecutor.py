'''
    We wanted something like Thread and Process Pool Exceutors
    but for async function
'''
import asyncio
import logging
from concurrent.futures import Executor

LOGGER = logging.getLogger(__name__)


class NotRunningException(Exception):
    ''' Called when a running pool is required '''


class AsyncPoolExecutor(Executor):
    '''
        This object can be called with async functions and you
        can limit the number of workers with max_workers.
        It maintains a queue of work of max_size.
    '''

    def __init__(self, loop=None, max_workers=None, max_size=0):
        self.max_workers = max_workers if max_workers else 4
        self.running = False
        self.loop = loop if loop else asyncio.get_event_loop()
        self.queue = asyncio.Queue(maxsize=max_size, loop=self.loop)
        self.workers = []

    def start(self):
        ''' called by aenter '''
        LOGGER.debug('starting...')
        self.running = True
        for n_id in range(self.max_workers):
            worker = asyncio.ensure_future(self.worker(n_id))
            self.workers.append(worker)

    async def worker(self, n_id):
        ''' worker called a task '''
        LOGGER.debug('working: %s', n_id)
        while self.running is True:
            try:
                await self.perform(n_id)
            except asyncio.CancelledError:
                return

    async def perform(self, n_id):
        ''' called by a worker to get queue item '''
        LOGGER.debug('pulling from queue: %s', n_id)
        item = await self.queue.get()
        results, func, args, kwargs = item
        try:
            result = await func(*args, **kwargs)
            results.set_result(result)
        except Exception as ex:  # pylint: disable=W0703
            results.set_exception(ex)
        finally:
            self.queue.task_done()

    def submit(self, fn, *args, **kwargs):  # pylint: disable=W0221
        ''' part of the executor api '''
        if self.running is False:
            raise NotRunningException()
        result = self.loop.create_future()
        LOGGER.debug('adding to queue...')
        self.queue.put_nowait((result, fn, args, kwargs))
        return result

    def map(self, func, *iterables):  # pylint: disable=W0221
        ''' part of the executor api '''
        if self.running is False:
            raise NotRunningException()
        results = []
        args = zip(*iterables)
        LOGGER.debug('args... %r', args)
        for line in args:
            results.append(self.submit(func, *line))
        return results

    async def shutdown(self, wait=True):
        '''
            part of the executor api
            called by aexit
        '''
        LOGGER.debug('shutting down...')
        if wait:
            LOGGER.debug('joining...')
            await self.queue.join()
        self.running = False
        try:
            while True:
                LOGGER.debug('cancelling queue contents...')
                item = self.queue.get_nowait()
                item[0].cancel()
                self.queue.task_done()
        except asyncio.QueueEmpty:
            pass
        LOGGER.debug('cancelling workers...')
        for task in self.workers:
            task.cancel()
        LOGGER.debug('gathering workers...')
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
        LOGGER.debug('shutdown')

    async def __aenter__(self):
        ''' This makes us an async contextmanager '''
        self.start()
        return self

    async def __aexit__(self, *args):
        ''' This is called when the with is up '''
        await self.shutdown()

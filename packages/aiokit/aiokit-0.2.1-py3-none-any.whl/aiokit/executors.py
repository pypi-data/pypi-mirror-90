import asyncio
import logging
import multiprocessing
import os
import signal
import time
from functools import partial
from typing import (
    Callable,
    List,
    Optional,
    Union,
)

import uvloop

from .aiothing import AioThing

logger = logging.getLogger('aiokit.executors')


class MultiprocessAsyncExecutor:
    def __init__(
        self,
        create_aiothing: Optional[Union[Callable[[int], AioThing], partial]] = None,
        create_aiothings: Optional[List[Union[Callable[[int], AioThing], partial]]] = None,
        shards: List = None,
    ):
        if create_aiothing and create_aiothings:
            raise RuntimeError('`create_aiothing` and `create_aiothings` cannot be set both')
        if not create_aiothing and not create_aiothings:
            raise RuntimeError('`create_aiothing` or `create_aiothings` should be set')
        if create_aiothings and shards and len(create_aiothings) != len(shards):
            raise RuntimeError('length of `shards` and `create_aiothings` should be the same')

        if create_aiothings and not shards:
            shards = list(range(len(create_aiothings)))

        if create_aiothing and not shards:
            raise RuntimeError('`create_aiothing` requires shards')

        self._shutting_down = False
        self.processes = []

        if create_aiothing:
            create_aiothings = [create_aiothing] * len(shards)

        for create_aiothing, shard in zip(create_aiothings, shards):
            process = multiprocessing.Process(target=self._run_loop, args=(create_aiothing, shard,))
            process.daemon = True
            self.processes.append(process)

    def stop_children(self, signum):
        for process in self.processes:
            try:
                os.kill(process.pid, signum)
            except ProcessLookupError:
                pass

    def start(self):
        for process in self.processes:
            process.start()
        for sig in (signal.SIGTERM, signal.SIGINT):
            old_handler = signal.getsignal(sig)

            if old_handler and old_handler is not signal.default_int_handler:
                def new_handler(signum, frame):
                    old_handler(signum, frame)
                    self.stop_children(signum)
            else:
                def new_handler(signum, frame):
                    self.stop_children(signum)

            signal.signal(sig, new_handler)

    def join(self):
        while True:
            for process in self.processes:
                if process.exitcode is not None:
                    self.stop_children(signal.SIGTERM)
                    for process_to_join in self.processes:
                        process_to_join.join()
                    return
            time.sleep(1.0)

    def _run_loop(self, create_aiothing, shard):
        try:
            uvloop.install()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            aiothing = create_aiothing(shard)
            loop.run_until_complete(aiothing.start_and_wait())
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(e)
            raise

import asyncio

class AsyncTimer:
    def __init__(self, interval: float, callback: callable):
        self._interval = interval
        self._callback = callback
        self._task = None

    async def _run_timer(self):
        await asyncio.sleep(self._interval)
        await self._callback()

    async def __aenter__(self):
        self.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.cancel()

    def start(self):
        if not self._task:
            self._task = asyncio.create_task(self._run_timer())

    def cancel(self):
        if self._task:
            self._task.cancel()
            self._task = None

    def is_running(self):
        return self._task and not self._task.done()
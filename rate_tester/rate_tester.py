import argparse
import asyncio
from typing import NoReturn

from httpx import AsyncClient


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


class RateTester:

    __slots__ = [
        "_rate",
        "_interval",
        "_is_running",
        "_concurrent_workers",
        "_stop_event",
        "_client",
        "_url",
        "_header",
    ]

    def __init__(self, rate: int, url: str, header: dict = None, interval: int = 1):
        self._rate: int = rate
        self._interval: int = interval
        self._is_running: bool = False
        self._concurrent_workers: int = 0
        self._stop_event: asyncio.Event = asyncio.Event()
        self._client: AsyncClient = AsyncClient()
        self._url: str = url
        self._header: dict = header

    async def _perform(self) -> NoReturn:
        await self._client.get(self._url, headers=self._header)

    async def _scheduler(self) -> NoReturn:
        while self._is_running:
            for _ in range(self._rate):
                asyncio.create_task(self._worker())
            await asyncio.sleep(self._interval)

    async def _worker(self) -> NoReturn:
        self._concurrent_workers += 1
        await self._perform()
        self._concurrent_workers -= 1
        if not self._is_running and self._concurrent_workers == 0:
            self._stop_event.set()

    async def stop(self) -> NoReturn:
        self._is_running = False
        if self._concurrent_workers != 0:
            await self._stop_event.wait()

    async def start(self) -> NoReturn:
        self._is_running = True
        await self._scheduler()


def main(rps: int, url: str, authorization: str = None, token: str = None) -> NoReturn:
    if not authorization:
        tester = RateTester(rps, url)
    elif not authorization and token:
        raise ValidationError("No authorization name")
    else:
        header = {authorization: token}
        tester = RateTester(rps, url, header)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(tester.start())
    except KeyboardInterrupt:
        loop.run_until_complete(tester.stop())
        loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rps", required=True, type=int, help="Required rps")
    parser.add_argument(
        "--authorization", required=False, type=str, help="name of authorization header"
    )
    parser.add_argument("--token", required=False, type=str, help="authorization token")
    parser.add_argument("--url", required=True, type=str, help="url")
    args = parser.parse_args()
    main(args.rps, args.url, args.authorization, args.token)

from urllib.error import URLError
from urllib.request import urlopen, Request
import websockets
import asyncio
import sys


class MissingArguments(Exception):
    def __init__(self):
        super().__init__("There are missing arguments. Please use the format:\n cliweb.py [ws/http] [url]")


class UnknownURLScheme(Exception):
    def __init__(self, url):
        super().__init__(f"Unknown url scheme: {url}")


async def _valid_url(url):
    if "http://" or "https://" or "ws://" or "wss://" in url:
        return
    else:
        raise UnknownURLScheme(url)


async def _http_request(url: str):
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('server unreachable: ', e.reason)
        elif hasattr(e, 'code'):
            print('there was an error: ', e.code)
    else:
        return {
            "url": response.url,
            "headers": response.headers.as_string(),
            "status": response.status,
            "content": response.read()
        }


async def _websocket_connection(url):
    async with websockets.connect(url) as ws:
        await _websocket_handler(ws)


async def _websocket_handler(ws):
    try:
        async for i in ws:
            print(i)
    except KeyboardInterrupt:
        return


async def main():
    if len(sys.argv) < 3:
        raise MissingArguments
    await _valid_url(str(sys.argv[2]))
    print("CLIPython")
    print("-"*15)
    if sys.argv[1] == "ws":
        if not ":" in sys.argv[2]:
            raise MissingArguments
        print("start socket connection")
        await _websocket_connection(sys.argv[2])
    if sys.argv[1] == "http":
        print("start http request")
        print(await _http_request(sys.argv[2]))


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()

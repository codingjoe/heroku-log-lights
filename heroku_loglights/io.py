import asyncio
import json

import aiohttp
import math

from heroku_loglights import Log

queue = asyncio.Queue(30)

log_config = {
    "dyno": "router",
    "source": "heroku",
    "tail": True
}


class COLORS:
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[4m'

async def get_stream_url(app_name, token):
    url = 'https://api.heroku.com/apps/%s/log-sessions' % app_name
    with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': 'Bearer %s' % token
        }
        async with session.post(url, data=json.dumps(log_config), headers=headers) as response:
            if response.status == 201:
                data = await response.json()
                return data['logplex_url']
            else:
                raise IOError


async def read_stream(stream_url: str):
    log = b''
    print('Reading stream: %s' % stream_url)
    with aiohttp.ClientSession() as session:
        async with session.get(stream_url) as response:
            while True:
                chunk = await response.content.read(1)
                if not chunk:
                    break
                if chunk == b'\n':
                    await write_to_queue(log)
                    log = b''
                else:
                    log += chunk


async def write_to_queue(log: bytes):
    await queue.put(Log(log.decode('utf-8')))


async def print_log():
    while True:
        log = await queue.get()
        if log.service < 10:
            color = COLORS.GREEN
        elif log.service < 100:
            color = COLORS.BLUE
        elif log.service < 1000:
            color = COLORS.YELLOW
        else:
            color = COLORS.RED
        seconds = math.ceil(log.service / 1000)
        print(color + "{:>30}".format('')[:seconds] + COLORS.DEFAULT + "{:>30}".format('')[seconds:] + str(log))

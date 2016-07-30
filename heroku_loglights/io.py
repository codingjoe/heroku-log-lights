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


@asyncio.coroutine
def get_stream_url(app_name, token):
    url = 'https://api.heroku.com/apps/%s/log-sessions' % app_name
    with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': 'Bearer %s' % token
        }
        response = yield from session.post(url, data=json.dumps(log_config), headers=headers)
        if response.status == 201:
            data = yield from response.json()
            return data['logplex_url']
        else:
            raise IOError


@asyncio.coroutine
def read_stream(app_name, auth_token):
    while True:
        stream_url = yield from get_stream_url(app_name, auth_token)
        print('Reading stream: %s' % stream_url)
        log = b''
        with aiohttp.ClientSession() as session:
            response = yield from session.get(stream_url)
            while True:
                try:
                    chunk = yield from response.content.read(1)
                except aiohttp.ServerDisconnectedError:
                    break
                if not chunk:
                    break
                if chunk == b'\n':
                    yield from write_to_queue(log)
                    log = b''
                else:
                    log += chunk


@asyncio.coroutine
def write_to_queue(log: bytes):
    yield from queue.put(Log(log.decode('utf-8')))


@asyncio.coroutine
def print_log():
    while True:
        log = yield from queue.get()
        if log.service < 30:
            color = COLORS.GREEN
        elif log.service < 100:
            color = COLORS.BLUE
        elif log.service < 1000:
            color = COLORS.YELLOW
        else:
            color = COLORS.RED
        seconds = math.ceil(math.log(log.service, 1.4101)) % 30
        print(color + "{:>30}".format('')[:seconds] + COLORS.DEFAULT + "{:>30}".format('')[seconds:] + str(log))


@asyncio.coroutine
def print_matrix(matrix):
    x = 0
    while True:
        log = yield from queue.get()
        if log.service < 30:
            color = 0, 255, 0
        elif log.service < 100:
            color = 0, 0, 255
        elif log.service < 1000:
            color = 0, 255, 255
        else:
            color = 255, 0, 0
        seconds = math.ceil(math.log(log.service, 1.4101)) % 30
        for y in range(int(matrix.height * seconds/30)):
            matrix.SetPixel(x, matrix.height-y, *color)
        x += 1
        x %= matrix.width

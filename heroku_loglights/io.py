import asyncio
import json
import math

import aiohttp

from heroku_loglights import Log, HEROKU_ROUTER_TIMEOUT

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
    async with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': 'Bearer %s' % token
        }
        response = await session.post(url, data=json.dumps(log_config), headers=headers)
        if response.status == 201:
            data = await response.json()
            return data['logplex_url']
        else:
            raise IOError


async def read_stream(slots, app_name, auth_token):
    while True:
        try:
            stream_url = await get_stream_url(app_name, auth_token)
        except IOError:
            continue
        else:
            print('Reading stream: %s' % stream_url)
        async with aiohttp.ClientSession() as session:
            response = await session.get(stream_url)
            try:
                async for line in response.content:
                    try:
                        log = Log(line.decode())
                    except ValueError:
                        pass
                    else:
                        await print_log(log)
                        await write_slots(slots, log)

            except aiohttp.ServerDisconnectedError:
                pass


async def print_log(log):
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


async def write_slots(slots, log):
    try:
        i = slots.index([None, 0])
        slots[i] = [log, 0]
    except ValueError:
        print("No more slots. Log dropped: %s" % log)


async def print_matrix(matrix, slots):
    cs = 255 / matrix.height
    while True:
        for col, slot in enumerate(slots, start=1):
            col = matrix.width / 2 + (int(col / 2) if col % 2 else col / -2)
            if slot[0] is not None:
                try:
                    height = math.ceil(math.log(slot[1], HEROKU_ROUTER_TIMEOUT) * matrix.height)
                except ValueError:
                    pass
                else:
                    for y in range(height):
                        if 300 > slot[0].status >= 200:
                            color = int(0 + cs * y), int(255 - cs * y), 0
                        elif 400 > slot[0].status >= 300:
                            color = int(0 + cs * y), 0, int(255 - cs * y)
                        elif 500 > slot[0].status >= 400:
                            color = 255, 255, 0
                        elif slot[0].status >= 500:
                            color = 255, 0, 0
                        else:
                            color = 0, 0, 0
                        try:
                            matrix.SetPixel(col, matrix.height - y, *color)
                        except Exception:
                            pass
                if slot[0].service >= slot[1]:
                    slot[1] += 10
                else:
                    for row in range(matrix.height):
                        matrix.SetPixel(col, row, 0, 0, 0)
                    slot[0] = None
                    slot[1] = 0

        await asyncio.sleep(0.01)

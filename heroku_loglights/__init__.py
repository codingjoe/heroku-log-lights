"""Heroku Log Lights is a visualisation of Heroku router logs for an LED matrix."""
import re

VERSION = (0, 1, 0)

__version__ = '.'.join(str(i) for i in VERSION)
__author__ = 'Johannes Hoppe'
__licence__ = """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>"""

_example = '2016-05-27T13:35:16.153374+00:00 heroku[router]: at=info method=POST path="/api/import/closeio/" host=backend.thermondo.de request_id=2388ebb8-fe62-4834-aa01-d1aca2f210ff fwd="54.203.52.130" dyno=web.13 connect=0ms service=158ms status=200 bytes=488'


HEROKU_ROUTER_TIMEOUT = 30000

class Log:
    PATTERN = (
        r'(?P<year>\d{4})'
        r'-(?P<month>[01]\d)'
        r'-(?P<day>[0-3]\d)'
        r'T(?P<hour>[0-2]\d)'
        r':(?P<minute>[0-5]\d)'
        r':(?P<second>[0-5]\d)'
        r'\.\d+(?P<tz>[+-][0-2]\d:[0-5]\d|Z)'
        r' heroku\[router\]:'
        r' at=(?P<at>[^ ]+)'
        r' method=(?P<method>[^ ]+)'
        r' path="(?P<path>[^"]+)"'
        r' host=(?P<host>[^ ]+)'
        r' request_id=(?P<request_id>[^ ]+)'
        r' fwd=(?P<fwd>[^ ]+)'
        r' dyno=(?P<dyno>[^ ]+)'
        r' connect=(?P<connect>[^ ]+)'
        r' service=(?P<service>\d+)ms'
        r' status=(?P<status>\d+)'
        r' bytes=(?P<bytes>[^ ]+)'
    )

    def __init__(self, log_str: str):
        args = re.match(self.PATTERN, log_str).groupdict()
        self.status = int(args.pop('status'))
        self.service = int(args.pop('service'))
        for key, value in args.items():
            setattr(self, key, value)

    def __str__(self):
        return "{service:>5}ms /w {status} @ {path}".format(
            status=self.status,
            service=self.service,
            path=self.path,
        )

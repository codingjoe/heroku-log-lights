"""Heroku Log Lights is a visualisation of Heroku router logs for an LED matrix."""
import argparse
import asyncio
import functools
import logging
import os
import signal
import sys

from heroku_loglights.io import read_stream, print_log

logger = logging.getLogger('heroku_loglights')


def get_args():
    """Setup argument parser and return parsed arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__.strip()
    )
    parser.add_argument('-a', '--app', dest='app', metavar='HEROKU_APP', type=str,
                        help='Name of the target Heroku app.')
    parser.add_argument('-t', '--token', dest='token', metavar='AUTH_TOKEN', type=str,
                        default=None, help='Heroku AUTH token.')
    parser.add_argument('-v', dest='verbose', action='store_const',
                        const=logging.DEBUG, default=logging.WARNING,
                        help='verbose mode (default: off)')
    return parser.parse_args()


def main():
    args = get_args()

    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(args.verbose)

    app_name = args.app
    auth_token = args.token
    if auth_token in [None, '']:
        auth_token = os.environ.get('HEROKU_AUTH_TOKEN')
    if auth_token in [None, '']:
        raise RuntimeError('Please specify "HEROKU_AUTH_TOKEN" in your enivorment or add the token using "--token".')

    def ask_exit(signame):
        print("Got signal %s: exit" % signame)
        print("Cleaning up...")
        loop.stop()
        print("Done!")

    loop = asyncio.get_event_loop()
    asyncio.Task(read_stream(app_name, auth_token))
    asyncio.Task(print_log())

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(ask_exit, signame))
    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    sys.exit(main())

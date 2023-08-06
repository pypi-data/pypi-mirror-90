"""An interactive RCON shell."""

from argparse import ArgumentParser, Namespace
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from socket import timeout

from rcon.errorhandler import ErrorHandler
from rcon.exceptions import RequestIdMismatch
from rcon.rconclt import get_credentials
from rcon.readline import CommandHistory
from rcon.config import CONFIG_FILE, LOG_FORMAT
from rcon.console import PROMPT, rconcmd


__all__ = ['get_args', 'main']

ERRORS = (
    (ConnectionRefusedError, 'Connection refused.', 3),
    ((TimeoutError, timeout), 'Connection timeout.', 4),
    (RequestIdMismatch, 'Unexpected request ID mismatch.', 5)
)
LOGGER = getLogger('rconshell')


def get_args() -> Namespace:
    """Parses and returns the CLI arguments."""

    parser = ArgumentParser(description='An interactive RCON shell.')
    parser.add_argument('server', nargs='?', help='the server to connect to')
    parser.add_argument('-c', '--config', type=Path, metavar='file',
                        default=CONFIG_FILE, help='the configuration file')
    parser.add_argument('-p', '--prompt', default=PROMPT, metavar='PS1',
                        help='the shell prompt')
    return parser.parse_args()


def main() -> None:
    """Runs the RCON shell."""

    args = get_args()
    basicConfig(level=INFO, format=LOG_FORMAT)

    if args.server:
        host, port, passwd = get_credentials(args)
    else:
        host = port = passwd = None

    with ErrorHandler(ERRORS, LOGGER):
        with CommandHistory(LOGGER):
            rconcmd(host, port, passwd, prompt=args.prompt)

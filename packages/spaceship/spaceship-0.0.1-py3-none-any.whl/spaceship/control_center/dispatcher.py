import argparse
import logging
import sys

from spaceship.launchpad import launch


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
_logger = logging.getLogger("CONTROL CENTER")


COMMANDS = ("launch",)


def control() -> None:
    parser = argparse.ArgumentParser()

    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command:
        _subparsers = parser.add_subparsers()
        if command == "launch":
            launch(parser=_subparsers.add_parser("launch"), logger=_logger.getChild("LAUNCHER"))
    else:
        parser.add_argument("command", choices=COMMANDS, nargs="?",
                            help="Give a direct command to your ship.")
        parser.parse_args(["--help"])

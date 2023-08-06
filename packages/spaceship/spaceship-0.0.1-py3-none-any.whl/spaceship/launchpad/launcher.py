import argparse
import logging
import sys
import time


def _initiate_countdown(countdown: int, logger: logging.Logger) -> None:
    logger.info("Activate main engine hydrogen burnoff system")
    time.sleep(1)
    logger.info(f"Countdown before the start. Time T-{countdown} seconds.")
    for i in range(countdown, 0, -1):
        logger.info(i)
        time.sleep(1)
    logger.info("Main engine start")
    time.sleep(1)


def launch(*, parser: argparse.ArgumentParser, logger: logging.Logger) -> None:
    parser.add_argument("--countdown", nargs="?", type=int, const=10,
                        help="Count before the start. Default count is %(const)s.")
    args = parser.parse_args(sys.argv[2:])

    countdown = args.countdown

    if countdown:
        _initiate_countdown(countdown, logger)
    logger.info("Solid rocket booster ignition and liftoff!")

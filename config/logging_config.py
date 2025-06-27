

import logging

def setup_logging(level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=level,
        format="[{asctime}] {levelname:<8} {name:<20} {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

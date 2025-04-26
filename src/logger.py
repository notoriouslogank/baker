import logging

from rich.logging import RichHandler


def setup_logger(
    name: str = __name__, level=logging.INFO, verbose: bool = False, quiet=False
) -> logging.Logger:
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:

        rich_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_level=True,
            show_path=True,
        )
        formatter = logging.Formatter("%(message)s")
        rich_handler.setFormatter(formatter)
        logger.addHandler(rich_handler)
    return logger

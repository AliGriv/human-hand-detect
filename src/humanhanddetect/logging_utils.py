from __future__ import annotations
from loguru import logger
import sys


_LOGGING_CONFIGURED = False


def setup_logging(verbose: bool = False) -> None:
    """
    Configure the Loguru logger for the entire package.
    Should be called once at application startup (e.g. in CLI main()).

    Parameters
    ----------
    verbose : bool
        If True, use DEBUG level. Otherwise INFO.
    """
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return  # Prevent adding multiple handlers

    # Remove default handler to avoid duplicates
    logger.remove()

    logger.add(
        sys.stderr,
        level="DEBUG" if verbose else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
    )

    # Message to indicate logging has been set up
    if verbose:
        logger.debug("Logging configured to DEBUG level.")
    else:
        logger.info("Logging configured to INFO level.")

    _LOGGING_CONFIGURED = True


def get_logger(name: str = None):
    """
    Retrieve a logger instance.

    Parameters
    ----------
    name : str
        Optional module-specific name. If provided, the logger will
        include it in its context, but otherwise the global logger is returned.

    Returns
    -------
    loguru.Logger
    """
    if name:
        return logger.bind(module=name)
    return logger

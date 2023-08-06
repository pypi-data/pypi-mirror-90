import logging
import os
import sys
from typing import List

_narration_loggers_configured = {}
_narration_loggers_enabled = {}


def get_debug_logger(
    name: str = None,
    env_name: str = "DEBUG",
    env_value_default: str = "0",
    env_value_enabled: str = "1",
    level=logging.DEBUG,
):
    enabled = os.environ.get(env_name, env_value_default) == env_value_enabled
    return _get_debug_logger(name=name, enabled_override=enabled, level=level)


def is_debug_logger_enabled(name: str = None):
    global _narration_loggers_enabled
    return _narration_loggers_enabled.get(name, False)


def configure_debug_loggers(names: List[str] = [], enabled: bool = None, level=logging.DEBUG):
    for name in names:
        _configure_debug_logger_once(name=name, enabled=enabled, level=level)


def _get_debug_logger(name: str = None, enabled_override: bool = None, level: int = logging.DEBUG):
    configure_debug_loggers(names=[name], enabled=enabled_override, level=level)
    return logging.getLogger(name)


def _configure_debug_logger_once(name=None, enabled: bool = None, level=logging.DEBUG):
    global _narration_loggers_configured
    global _narration_loggers_enabled

    logger = logging.getLogger(name)

    # Do not reconfigure if enabled has not changed
    if _narration_loggers_configured.get(name, None) is not None:
        if enabled is None:
            return
        if not enabled == logger.disabled:
            return

    logger.disabled = not enabled
    logger.setLevel(level if enabled else logging.CRITICAL)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(name)s:PID%(process)d:T%(thread)d:%(levelname)s:%(message)s"
        )
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info(f"{name} _debug logger activated")

    _narration_loggers_configured[name] = True
    _narration_loggers_enabled[name] = enabled

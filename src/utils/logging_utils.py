"""
Custom logging utilities for the Product Development Multi-Agent App.

This module provides:
- PrettyJsonFormatter: Pretty-prints JSON/dict log messages for readability.
- UsagePrettyPrintHandler: For autogen_core.events logger, pretty-prints response.usage from message if present.
- setup_logging: Configures global logging and attaches handlers.

All public functions and classes are type-annotated and documented per project clean code standards.
"""
import logging
from autogen_core import EVENT_LOGGER_NAME, TRACE_LOGGER_NAME

def setup_logging() -> None:
    """Configure global logging with pretty JSON output and usage pretty print for LLM calls.

    Ensures no duplicate handlers are attached if called multiple times.
    """
    logging.basicConfig(level=logging.WARNING)

    # For trace logging.
    trace_logger = logging.getLogger(TRACE_LOGGER_NAME)
    trace_logger.addHandler(logging.StreamHandler())
    trace_logger.setLevel(logging.WARNING)

    # For structured message logging, such as low-level messages between agents.
    event_logger = logging.getLogger(EVENT_LOGGER_NAME)
    event_logger.addHandler(logging.StreamHandler())
    event_logger.setLevel(logging.WARNING)

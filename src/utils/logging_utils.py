"""
Custom logging utilities for the Product Development Multi-Agent App.

This module provides:
- PrettyJsonFormatter: Pretty-prints JSON/dict log messages for readability.
- UsagePrettyPrintHandler: For autogen_core.events logger, pretty-prints response.usage from message if present.
- setup_logging: Configures global logging and attaches handlers.

All public functions and classes are type-annotated and documented per project clean code standards.
"""
import logging
import json
import sys
from typing import Any
from autogen_core import EVENT_LOGGER_NAME


class PrettyJsonFormatter(logging.Formatter):
    """Formatter that pretty-prints JSON/dict log messages for readability.

    Args:
        fmt (str): Log message format string.
        datefmt (str): Date format string.
    """
    def format(self, record: logging.LogRecord) -> str:
        msg: Any = record.getMessage()
        try:
            if isinstance(msg, str) and msg.strip().startswith('{'):
                parsed = json.loads(msg)
                msg = json.dumps(parsed, indent=2, ensure_ascii=False)
        except Exception as exc:
            logging.getLogger(__name__).debug(f"PrettyJsonFormatter failed to parse message as JSON: {exc}")
        return f"{self.formatTime(record)} {record.levelname:<8} {record.name}: {msg}"


LLM_USAGE_HEADER = "\n--- LLM Usage ---"
LLM_USAGE_FOOTER = "--- End Usage ---\n"

class UsagePrettyPrintHandler(logging.Handler):
    """Handler for autogen_core.events logger that pretty-prints response.usage from message if present.

    Only triggers for EVENT_LOGGER_NAME logs. Prints usage block if found in response.
    """
    def emit(self, record: logging.LogRecord) -> None:
        if record.name != EVENT_LOGGER_NAME:
            return
        msg: Any = record.getMessage()
        try:
            if isinstance(msg, str) and msg.strip().startswith('{'):
                parsed = json.loads(msg)
                response = parsed.get('response')
                if isinstance(response, dict) and 'usage' in response:
                    usage = response['usage']
                    print(LLM_USAGE_HEADER)
                    print(json.dumps(usage, indent=2, ensure_ascii=False))
                    print(LLM_USAGE_FOOTER)
        except Exception as exc:
            logging.getLogger(__name__).debug(f"UsagePrettyPrintHandler failed to parse usage: {exc}")

def setup_logging() -> None:
    """Configure global logging with pretty JSON output and usage pretty print for LLM calls.

    Ensures no duplicate handlers are attached if called multiple times.
    """
    root_logger = logging.getLogger()
    # Remove only StreamHandlers to avoid interfering with other handlers
    root_logger.handlers = [h for h in root_logger.handlers if not isinstance(h, logging.StreamHandler)]
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(PrettyJsonFormatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Add usage pretty print handler for EVENT_LOGGER_NAME if not already present
    event_logger = logging.getLogger(EVENT_LOGGER_NAME)
    if not any(isinstance(h, UsagePrettyPrintHandler) for h in event_logger.handlers):
        event_logger.addHandler(UsagePrettyPrintHandler())
    event_logger.propagate = True

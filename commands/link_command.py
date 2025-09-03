# commands/link_command.py
from types import ModuleType
from typing import Any


def execute(config: ModuleType, message: str) -> str:
    """Returns the response for the !link command."""
    return str(config.CHAT_COMMANDS["!link"])

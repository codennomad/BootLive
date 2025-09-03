# commands/discord_command.py
from types import ModuleType


def execute(config: ModuleType, message: str) -> str:
    """Returns the response for the !discord command."""
    return str(config.CHAT_COMMANDS["!discord"])

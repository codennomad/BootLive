import json
import os
import logging
from types import ModuleType
from typing import Dict, Set


def load_banned_users() -> Set[str]:
    """Load banned users from file."""
    banned_file = "banned_users.json"
    if os.path.exists(banned_file):
        try:
            with open(banned_file, "r") as f:
                data = json.load(f)
                return set(data.get("banned_users", []))
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading banned users: {e}")
    return set()


def save_banned_users(banned_users: Set[str]) -> None:
    """Save banned users to file."""
    banned_file = "banned_users.json"
    try:
        with open(banned_file, "w") as f:
            json.dump({"banned_users": list(banned_users)}, f, indent=2)
    except IOError as e:
        logging.error(f"Error saving banned users: {e}")


def execute(config: ModuleType, message: str) -> str:
    """Execute the ban command."""
    parts = message.split()
    if len(parts) < 2:
        return "Usage: !ban <username>"

    username = parts[1].strip()
    if not username:
        return "Please provide a valid username to ban."

    # Load current banned users
    banned_users = load_banned_users()

    if username in banned_users:
        return f"User {username} is already banned."

    # Add user to banned list
    banned_users.add(username)
    save_banned_users(banned_users)

    logging.info(f"User {username} has been banned.")
    return f"User {username} has been banned from the chat."

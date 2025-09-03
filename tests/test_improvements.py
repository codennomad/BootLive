import unittest
from types import ModuleType
from unittest.mock import MagicMock, patch

import config
from command_handler import (
    handle_command,
    load_command,
    unload_command,
    reload_command,
    load_commands,
)
import command_handler


class TestImprovements(unittest.TestCase):
    def setUp(self) -> None:
        # Reset commands before each test
        load_commands()
        # Reset global command cooldown
        command_handler.last_command_time = 0

    @patch("command_handler.time.time")
    def test_global_command_cooldown(self, mock_time: MagicMock) -> None:
        """Tests that the global command cooldown is working."""
        mock_time.side_effect = [1000.0, 1000.5]  # Second call is within cooldown

        # First command should work
        response = handle_command("!link", config, "user1", "!link")
        self.assertIsNotNone(response)

        # Second command should be ignored due to cooldown
        response = handle_command("!discord", config, "user2", "!discord")
        self.assertIsNone(response)

    def test_command_permissions(self) -> None:
        """Tests that the command permission system is working."""
        # Non-moderator should not be able to use !ban
        response = handle_command("!ban", config, "user1", "!ban user2")
        self.assertEqual(response, "You do not have permission to use this command.")

        # Moderator should be able to use !ban
        config.MODERATORS = ["user1"]
        response = handle_command("!ban", config, "user1", "!ban user2")
        self.assertNotEqual(response, "You do not have permission to use this command.")

    @patch("command_handler.time.time")
    def test_dynamic_command_loading(self, mock_time: MagicMock) -> None:
        """Tests that dynamic command loading, unloading, and reloading is working."""
        mock_time.side_effect = [
            1000.0,
            2000.0,
            3000.0,
        ]  # Different times to avoid cooldown

        # Unload the link command
        self.assertTrue(unload_command("link"))
        response = handle_command("!link", config, "user1", "!link")
        self.assertIsNone(response)

        # Load the link command
        self.assertTrue(load_command("link"))
        response = handle_command("!link", config, "user1", "!link")
        self.assertIsNotNone(response)

        # Reload the link command
        self.assertTrue(reload_command("link"))
        response = handle_command("!link", config, "user1", "!link")
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()

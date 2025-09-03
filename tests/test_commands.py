# tests/test_commands.py
import unittest
import config
from commands import link_command, discord_command, ban_command, unban_command


class TestCommands(unittest.TestCase):

    def test_link_command(self) -> None:
        """Tests that the link command returns the correct string."""
        expected_response = config.CHAT_COMMANDS["!link"]
        self.assertEqual(link_command.execute(config, "!link"), expected_response)

    def test_discord_command(self) -> None:
        """Tests that the discord command returns the correct string."""
        expected_response = config.CHAT_COMMANDS["!discord"]
        self.assertEqual(discord_command.execute(config, "!discord"), expected_response)

    def test_ban_command_usage(self) -> None:
        """Tests that the ban command returns usage when no username provided."""
        response = ban_command.execute(config, "!ban")
        self.assertEqual(response, "Usage: !ban <username>")

    def test_ban_command_with_username(self) -> None:
        """Tests that the ban command works with a username."""
        response = ban_command.execute(config, "!ban testuser")
        self.assertIn("testuser", response)

    def test_unban_command_usage(self) -> None:
        """Tests that the unban command returns usage when no username provided."""
        response = unban_command.execute(config, "!unban")
        self.assertEqual(response, "Usage: !unban <username>")


if __name__ == "__main__":
    unittest.main()

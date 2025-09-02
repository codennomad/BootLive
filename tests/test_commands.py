# tests/test_commands.py
import unittest
import config
from commands import link_command, discord_command

class TestCommands(unittest.TestCase):

    def test_link_command(self):
        """Tests that the link command returns the correct string."""
        expected_response = config.CHAT_COMMANDS['!link']
        self.assertEqual(link_command.execute(config), expected_response)

    def test_discord_command(self):
        """Tests that the discord command returns the correct string."""
        expected_response = config.CHAT_COMMANDS['!discord']
        self.assertEqual(discord_command.execute(config), expected_response)

if __name__ == '__main__':
    unittest.main()

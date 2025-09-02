# tests/test_command_handler.py
import unittest
import config
from command_handler import load_commands, handle_command, commands

class TestCommandHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the commands once for all tests in this class."""
        # Clear any previously loaded commands for a clean test environment
        commands.clear()
        load_commands()

    def test_commands_loaded(self):
        """Tests if the command handler correctly loads command modules."""
        # We expect !link and !discord to be loaded
        self.assertIn("!link", commands)
        self.assertIn("!discord", commands)
        # Check that the values are callable functions
        self.assertTrue(callable(commands["!link"]))
        self.assertTrue(callable(commands["!discord"]))

    def test_handle_known_command(self):
        """Tests handling a known, valid command."""
        response = handle_command("!link", config)
        expected_response = config.CHAT_COMMANDS["!link"]
        self.assertEqual(response, expected_response)

    def test_handle_unknown_command(self):
        """Tests handling an unknown command."""
        response = handle_command("!nonexistentcommand", config)
        self.assertIsNone(response)

    def test_handle_command_with_no_config(self):
        """Tests that commands fail gracefully if config is not passed (if they need it)."""
        # This tests that the command function is called and raises an error
        # because the config object we pass is empty.
        with self.assertRaises(AttributeError):
            handle_command("!link", type('EmptyConfig', (), {})())

if __name__ == '__main__':
    unittest.main()

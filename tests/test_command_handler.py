# tests/test_command_handler.py
import unittest
from unittest.mock import patch, MagicMock
import config
from command_handler import (
    has_permission,
    handle_command,
    load_command,
    unload_command,
    reload_command,
)


class TestCommandHandler(unittest.TestCase):

    def test_has_permission_moderator(self) -> None:
        """Tests that moderators have permission for moderator commands."""
        # Mock config with moderators list
        mock_config = MagicMock()
        mock_config.MODERATORS = ["test_moderator_id"]
        mock_config.COMMAND_PERMISSIONS = {"!ban": ["moderator"]}

        result = has_permission("test_moderator_id", "!ban", mock_config)
        self.assertTrue(result)

    def test_has_permission_non_moderator(self) -> None:
        """Tests that non-moderators don't have permission for moderator commands."""
        mock_config = MagicMock()
        mock_config.MODERATORS = ["other_moderator_id"]
        mock_config.COMMAND_PERMISSIONS = {"!ban": ["moderator"]}

        result = has_permission("regular_user_id", "!ban", mock_config)
        self.assertFalse(result)

    def test_has_permission_no_permission_required(self) -> None:
        """Tests that commands with no permission requirements work for everyone."""
        mock_config = MagicMock()
        mock_config.COMMAND_PERMISSIONS = {}

        result = has_permission("any_user_id", "!link", mock_config)
        self.assertTrue(result)

    @patch("command_handler.commands")
    @patch("command_handler.time.time")
    def test_handle_command_success(
        self, mock_time: MagicMock, mock_commands: MagicMock
    ) -> None:
        """Tests successful command handling."""
        mock_time.return_value = 1000.0

        # Mock command function
        mock_command_func = MagicMock(return_value="Command executed successfully")
        mock_commands.__contains__ = MagicMock(return_value=True)
        mock_commands.__getitem__ = MagicMock(return_value=mock_command_func)

        # Mock config
        mock_config = MagicMock()
        mock_config.COMMAND_PERMISSIONS = {}
        mock_config.GLOBAL_COMMAND_COOLDOWN_SECONDS = 0

        result = handle_command("!test", mock_config, "user_id", "!test")
        self.assertEqual(result, "Command executed successfully")

    @patch("command_handler.commands")
    def test_handle_command_not_found(self, mock_commands: MagicMock) -> None:
        """Tests handling of non-existent commands."""
        mock_commands.__contains__ = MagicMock(return_value=False)

        mock_config = MagicMock()

        result = handle_command("!nonexistent", mock_config, "user_id", "!nonexistent")
        self.assertIsNone(result)

    @patch("importlib.import_module")
    def test_load_command_success(self, mock_import: MagicMock) -> None:
        """Tests successful command loading."""
        mock_module = MagicMock()
        mock_module.execute = MagicMock()
        mock_import.return_value = mock_module

        result = load_command("test")
        self.assertTrue(result)

    @patch("importlib.import_module")
    def test_load_command_failure(self, mock_import: MagicMock) -> None:
        """Tests command loading failure."""
        mock_import.side_effect = ImportError("Module not found")

        result = load_command("nonexistent")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

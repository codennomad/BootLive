# tests/test_youtube_api.py
import unittest
from unittest.mock import patch, MagicMock
from youtube_api import get_live_chat_id, send_chat_message, get_own_channel_name

class TestYoutubeApi(unittest.TestCase):

    @patch('youtube_api.build')
    def test_get_live_chat_id_success(self, mock_build):
        """Tests getting a live chat ID successfully."""
        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {
            'items': [
                {
                    'liveStreamingDetails': {
                        'activeLiveChatId': 'test_chat_id'
                    }
                }
            ]
        }
        chat_id = get_live_chat_id(mock_youtube, 'test_video_id')
        self.assertEqual(chat_id, 'test_chat_id')

    @patch('youtube_api.build')
    def test_get_live_chat_id_no_video(self, mock_build):
        """Tests getting a live chat ID for a nonexistent video."""
        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {'items': []}
        chat_id = get_live_chat_id(mock_youtube, 'test_video_id')
        self.assertIsNone(chat_id)

    @patch('youtube_api.build')
    def test_get_live_chat_id_not_live(self, mock_build):
        """Tests getting a live chat ID for a video that is not a live stream."""
        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {
            'items': [
                {
                    'liveStreamingDetails': None
                }
            ]
        }
        chat_id = get_live_chat_id(mock_youtube, 'test_video_id')
        self.assertIsNone(chat_id)

    @patch('youtube_api.build')
    def test_send_chat_message(self, mock_build):
        """Tests the send_chat_message function."""
        mock_youtube = MagicMock()
        send_chat_message(mock_youtube, 'test_chat_id', 'Hello World')
        # Check that the insert method was called with the correct parameters
        mock_youtube.liveChatMessages().insert.assert_called_once_with(
            part='snippet',
            body={
                'snippet': {
                    'liveChatId': 'test_chat_id',
                    'type': 'textMessageEvent',
                    'textMessageDetails': {
                        'messageText': 'Hello World'
                    }
                }
            }
        )

    @patch('youtube_api.build')
    def test_get_own_channel_name_success(self, mock_build):
        """Tests getting the bot's own channel name successfully."""
        mock_youtube = MagicMock()
        mock_youtube.channels().list().execute.return_value = {
            'items': [
                {
                    'snippet': {
                        'title': 'Test Bot Channel'
                    }
                }
            ]
        }
        channel_name = get_own_channel_name(mock_youtube)
        self.assertEqual(channel_name, 'Test Bot Channel')

    @patch('youtube_api.build')
    def test_get_own_channel_name_no_channel(self, mock_build):
        """Tests getting the bot's own channel name when no channel is found."""
        mock_youtube = MagicMock()
        mock_youtube.channels().list().execute.return_value = {'items': []}
        channel_name = get_own_channel_name(mock_youtube)
        self.assertIsNone(channel_name)

if __name__ == '__main__':
    unittest.main()

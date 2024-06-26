import unittest
from unittest.mock import patch, MagicMock


class TestMain(unittest.TestCase):

    @patch('main.Configurator')
    @patch('main.Detector')
    def test_main_initialization(self, mock_detector, mock_configurator):
        mock_config_instance = MagicMock()
        mock_detector_instance = MagicMock()
        mock_configurator.return_value = mock_config_instance
        mock_detector.return_value = mock_detector_instance
        mock_configurator.assert_called_once()
        mock_detector.assert_called_once_with(mock_config_instance)
        mock_detector_instance.detect_threatening_objects.assert_called_once()


if __name__ == '__main__':
    unittest.main()

import os
import unittest
from unittest.mock import patch, MagicMock, call
from detection import Detector
from configuration import Configurator


class TestDetector(unittest.TestCase):

    def setUp(self):
        self.configurator = Configurator()
        self.detector = Detector(self.configurator)

    def test_folder_tree_manager(self):
        self.detector.folder_tree_manager()
        self.assertTrue(os.path.exists("Threatening_Objects"))

    @patch('cv2.imwrite')
    @patch('playsound.playsound')
    def test_save_frame_with_detection(self, mock_playsound, mock_imwrite):
        mock_results = MagicMock()
        mock_results.plot.return_value = 'annotated_image'
        self.detector.save_frame_with_detection(mock_results)
        mock_imwrite.assert_called_once()

    @patch('configuration.YOLO')
    @patch('cv2.VideoCapture')
    def test_detect_threatening_objects(self, mock_videocapture, mock_yolo):
        mock_model = mock_yolo.return_value
        mock_results = MagicMock()
        mock_boxes = MagicMock()
        mock_boxes.cls = MagicMock()
        mock_boxes.cls.item.return_value = 0
        mock_results.boxes = [mock_boxes]
        mock_model.predict.return_value = [mock_results]

        mock_capture = mock_videocapture.return_value
        mock_capture.read.side_effect = [(True, 'frame1'), (True, 'frame2'), (False, 'frame3')]

        with patch.object(self.detector, 'save_frame_with_detection', return_value=None) as mock_save_frame:
            self.detector.detect_threatening_objects()

            # Verify that the method is called twice, for 'frame1' and 'frame2'
            self.assertEqual(mock_save_frame.call_count,  2)
            mock_save_frame.assert_has_calls([call(mock_results), call(mock_results)])


if __name__ == '__main__':
    unittest.main()

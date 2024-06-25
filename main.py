from configuration import Configurator
from detection import Detector

configuration = Configurator()

detection = Detector(configuration)
detection.detect_threatening_objects()

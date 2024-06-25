import shutil
import cv2
import os
from playsound import playsound
from configuration import Configurator


class Detector:
    def __init__(self, configurator):

        self.configuration = configurator
        self.frame_counter = 1

    @staticmethod
    def folder_tree_manager():

        if os.path.exists("Threatening_Objects"):
            shutil.rmtree("Threatening_Objects")
        os.makedirs("Threatening_Objects")

    def save_frame_with_detection(self, results):

        filename = f"Threatening_Object_{self.frame_counter}.jpg"
        annotated_image = results.plot()
        cv2.imwrite(os.path.join("Threatening_Objects", filename), annotated_image)
        self.frame_counter += 1
        print("*** Threatening object detected - frame saved ***")
        playsound(self.configuration.notification_sound)

    def detect_threatening_objects(self):

        Detector.folder_tree_manager()
        try:
            while True:

                results_generator = self.configuration.used_model.predict(
                    self.configuration.video_source, show=True, stream=True,
                    conf=0.25, classes=self.configuration.user_selected_classes)

                for results in results_generator:
                    detected_objects = {}

                    for detection in results.boxes:
                        class_id = detection.cls.item()
                        class_name = self.configuration.used_model.names[class_id]
                        if class_name not in detected_objects:
                            detected_objects[class_name] = 1
                        else:
                            detected_objects[class_name] += 1

                    if self.configuration.user_selected_threat in detected_objects:
                        Detector.save_frame_with_detection(self, results)

                    if detected_objects:
                        print("*** Detected Objects:", detected_objects, " ***")

        except Exception as e:
            print("Detection error occurred:", e)


if __name__ == "__main__":
    configuration = Configurator()
    detector = Detector(configuration)
    detector.detect_threatening_objects()

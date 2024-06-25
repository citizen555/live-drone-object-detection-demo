import netifaces
from ultralytics import YOLO
from playsound import playsound


class Configurator:
    def __init__(self):

        self.ip_addresses = self.get_active_ip_addresses()

        self.user_selected_classes = [0, 1, 2, 3, 4, 5, 7, 8]
        # train - 6
        self.user_selected_threat = 'truck'

        self.used_model = YOLO('yolov8m.pt')

        self.video_source = 'rtmp://127.0.0.1:1935/live/stream'

        self.notification_sound = 'notification_sound.wav'

        # source = 'rtmp://127.0.0.1:1935/live/stream'
        # source = 'https://www.youtube.com/watch?v=MNn9qKG2UFI&list=PLcQZGj9lFR7y5WikozDSrdk6UCtAnM9mB' # test video
        # source = 'video_test.mp4'
        # source = 'https://www.youtube.com/watch?v=10dguZKFWV4' # wlodawa city livestream

    @staticmethod
    def get_active_ip_addresses():
        ip_addresses = {}
        for interface in netifaces.interfaces():
            addresses = netifaces.ifaddresses(interface)
            inet = addresses.get(netifaces.AF_INET)
            if inet:
                for addr in inet:
                    ip_addresses[interface] = addr['addr']
        return ip_addresses

    def display_and_choose_ip_address(self):
        if not self.ip_addresses:
            print("There are no available network interfaces with assigned IPv4 addresses.")
            return None

        print("Active network interfaces and their IP addresses:")

        for idx, (interface, ip) in enumerate(self.ip_addresses.items(), start=1):
            print(f"* {idx} * Network interface-{interface} IP address: {ip}")

        while True:
            try:
                print()
                choice = int(input("Select an interface number to use its IP address: "))
                if 1 <= choice <= len(self.ip_addresses):
                    selected_interface = list(self.ip_addresses.items())[choice - 1]
                    return selected_interface[1]
                else:
                    print("Incorrect selection, please try again.")
            except ValueError:
                print("Please enter a valid number.")


if __name__ == "__main__":
    config = Configurator()
    selected_ip = config.display_and_choose_ip_address()
    if selected_ip:
        print(f"Selected IP address: {selected_ip}")

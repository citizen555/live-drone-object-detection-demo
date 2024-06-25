import unittest
from configuration import Configurator


class TestConfigurator(unittest.TestCase):

    def setUp(self):
        self.configurator = Configurator()

    def test_ip_addresses_retrieval(self):
        ip_addresses = self.configurator.get_active_ip_addresses()
        self.assertIsInstance(ip_addresses, dict)
        for interface, ip in ip_addresses.items():
            self.assertIsInstance(interface, str)
            self.assertIsInstance(ip, str)

    def test_user_selected_classes(self):
        self.assertIsNotNone(self.configurator.user_selected_classes)

    def test_user_selected_threat(self):
        self.assertIsNotNone(self.configurator.user_selected_threat)

    def test_used_model(self):
        self.assertIsNotNone(self.configurator.used_model)


if __name__ == '__main__':
    unittest.main()

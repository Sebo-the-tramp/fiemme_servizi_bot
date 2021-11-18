import unittest

from new import send_message

class TestMessage(unittest.TestCase):
    def test_message(self):
        self.assertEqual("Hello World", "Hello World")

if __name__ == '__main__':
    unittest.main()
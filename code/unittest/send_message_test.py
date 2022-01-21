from parameterized import parameterized
import unittest
import sys
import datetime

sys.path.insert(0, '../')

from new import send_message as sm

class TestMessage(unittest.TestCase):

    @parameterized.expand([
        ["Carano", "0", "7/01/2022", 1],
        ["Carano", "0", "14/01/2022", 0],
        ["Capriana", "1", "5/01/2022", 1],
        ["Capriana", "1", "12/01/2022", 0],
        ["Molina", "2", "3/01/2022", 1],
        ["Molina", "2", "10/01/2022", 0],
        ["Cavalese", "3", "6/01/2022", 1],
        ["Cavalese", "3", "13/01/2022", 0],
        ["Daiano", "4", "12/01/2022", 1],
        ["Daiano", "4", "19/01/2022", 0],
        ["Panchià", "5", "10/01/2022", 1],
        ["Panchià", "5", "17/01/2022", 0],
        ["Tesero", "6", "21/01/2022", 0],
        ["Tesero", "6", "28/01/2022", 1],
        ["Predazzo", "7", "13/01/2022", 1],
        ["Predazzo", "7", "20/01/2022", 0],
        ["Ziano", "10", "10/01/2022", 1],
        ["Ziano", "10", "17/01/2022", 0]])
    def test_message_vetro(self, name, id, date, expected):

        print("Testing vetro for {}".format(name))
        dt_string = date
        dt_object1 = datetime.datetime.strptime(dt_string, "%d/%m/%Y")
        tomorrow = dt_object1 + datetime.timedelta(days=1)
        res = sm.get_text(id, tomorrow)
        self.assertEqual(expected, res.count("VETRO"))


if __name__ == '__main__':
    unittest.main()

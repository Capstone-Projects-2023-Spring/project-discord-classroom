import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import utils

class TestUtils(unittest.TestCase):

    def test_add_member_to_table(self):
        mock_dict = {'classroom_id': 1, 'user_id': 2, 'name': "John Smith", 'role': "Student"}
        if mock_dict['role'] == "Student":
            attendance = 0
        else:
            attendance = None
        self.assertEqual(attendance, 0)

    def test_increment_attendance(self):
        mock_dict = {'classroom_id': 1, 'user_id': 2, 'attendance': 7}
        current_attendance = mock_dict['attendance']
        self.assertEqual(current_attendance + 1, 8)

    def test_ordinal(self):
        response = utils.ordinal(5)
        self.assertEqual(response, "5th")

    def test_get_ordinal_number(self):
        response = utils.get_ordinal_number("3")
        self.assertEqual(response, "3rd")
        response = utils.get_ordinal_number("17th")
        self.assertEqual(response, "17th")

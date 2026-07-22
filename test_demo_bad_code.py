import unittest
from demo_bad_code import get_user_data

class TestGetUserData(unittest.TestCase):
    def setUp(self):
        self.users = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'}
        ]

    def test_get_user_data_found(self):
        """Test happy path where user is found."""
        user = get_user_data(self.users, 1)
        self.assertEqual(user, {'id': 1, 'name': 'Alice'})

    def test_get_user_data_not_found(self):
        """Test edge case where user is not found."""
        user = get_user_data(self.users, 3)
        self.assertIsNone(user)

    def test_get_user_data_empty_list(self):
        """Test edge case with an empty user list."""
        user = get_user_data([], 1)
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()

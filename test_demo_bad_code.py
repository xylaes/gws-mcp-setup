import unittest
from unittest.mock import patch
from demo_bad_code import get_user_data, process_payments, process_single_payment


class TestGetUserData(unittest.TestCase):
    def setUp(self):
        self.users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    def test_get_user_data_found(self):
        """Test happy path where user is found."""
        user = get_user_data(self.users, 1)
        self.assertEqual(user, {"id": 1, "name": "Alice"})

    def test_get_user_data_not_found(self):
        """Test edge case where user is not found."""
        user = get_user_data(self.users, 3)
        self.assertIsNone(user)

    def test_get_user_data_empty_list(self):
        """Test edge case with an empty user list."""
        user = get_user_data([], 1)
        self.assertIsNone(user)

    def test_get_user_data_dictionary(self):
        """Test happy path where users is a dictionary (optimized lookup)."""
        users_dict = {1: {"id": 1, "name": "Alice"}, 2: {"id": 2, "name": "Bob"}}
        user = get_user_data(users_dict, 1)
        self.assertEqual(user, {"id": 1, "name": "Alice"})

        # Test not found
        user_not_found = get_user_data(users_dict, 3)
        self.assertIsNone(user_not_found)


class TestProcessSinglePayment(unittest.TestCase):
    @patch("demo_bad_code.time.sleep", return_value=None)
    def test_process_single_payment_happy_path(self, mock_sleep):
        """Test process_single_payment with standard valid pricing."""
        item = {"price": 100}
        result = process_single_payment(item)
        self.assertEqual(result, 110.0)
        mock_sleep.assert_called_once_with(0.1)

    @patch("demo_bad_code.time.sleep", return_value=None)
    def test_process_single_payment_zero_price(self, mock_sleep):
        """Test process_single_payment with zero price."""
        item = {"price": 0}
        result = process_single_payment(item)
        self.assertEqual(result, 0.0)
        mock_sleep.assert_called_once_with(0.1)

    @patch("demo_bad_code.time.sleep", return_value=None)
    def test_process_single_payment_negative_price(self, mock_sleep):
        """Test process_single_payment with negative price (edge case)."""
        item = {"price": -50}
        result = process_single_payment(item)
        self.assertEqual(result, -55.0)
        mock_sleep.assert_called_once_with(0.1)


class TestProcessPayments(unittest.TestCase):
    def test_process_payments_normal(self):
        items = [{"price": 10}, {"price": 20}]
        total = process_payments(items)
        self.assertEqual(total, 33.0)

    def test_process_payments_empty(self):
        items = []
        total = process_payments(items)
        self.assertEqual(total, 0)


if __name__ == "__main__":
    unittest.main()

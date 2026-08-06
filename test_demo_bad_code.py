import unittest
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

class TestProcessPayments(unittest.TestCase):
    def test_process_payments_normal(self):
        items = [{"price": 10}, {"price": 20}]
        total = process_payments(items)
        self.assertEqual(total, 33.0)

    def test_process_payments_empty(self):
        items = []
        total = process_payments(items)
        self.assertEqual(total, 0)


class TestProcessSinglePayment(unittest.TestCase):
    def test_process_single_payment_normal(self):
        """Test happy path with an integer price."""
        item = {"price": 10}
        total = process_single_payment(item)
        self.assertEqual(total, 11.0)

    def test_process_single_payment_float(self):
        """Test happy path with a floating-point price."""
        item = {"price": 15.5}
        total = process_single_payment(item)
        self.assertEqual(total, 17.05)

    def test_process_single_payment_zero(self):
        """Test processing a payment where the price is zero."""
        item = {"price": 0}
        total = process_single_payment(item)
        self.assertEqual(total, 0.0)

    def test_process_single_payment_negative(self):
        """Test processing a payment with a negative price."""
        item = {"price": -10}
        total = process_single_payment(item)
        self.assertEqual(total, -11.0)

    def test_process_single_payment_missing_price_key(self):
        """Test that KeyError is raised when the price key is missing."""
        item = {"wrong_key": 10}
        with self.assertRaises(KeyError):
            process_single_payment(item)

    def test_process_single_payment_non_dict_input(self):
        """Test that TypeError is raised when input is not a dictionary."""
        with self.assertRaises(TypeError):
            process_single_payment(None)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock

# Mock google.auth.default to bypass credentials loading during import
with patch("google.auth.default", return_value=(MagicMock(), "mock-project-id")):
    import main


class TestDisableBilling(unittest.TestCase):

    @patch("main.billing_v1.CloudBillingClient")
    def test_disable_billing_success(self, mock_client_class):
        # Setup mock client instance
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        # Call the function
        project_id = "test-project-123"
        main.disable_billing(project_id)

        # Verify the API was called correctly
        expected_name = f"projects/{project_id}"

        # Verify update_project_billing_info was called
        mock_client.update_project_billing_info.assert_called_once()

        # Get the arguments it was called with
        kwargs = mock_client.update_project_billing_info.call_args.kwargs
        self.assertEqual(kwargs["name"], expected_name)
        self.assertEqual(kwargs["project_billing_info"].billing_account_name, "")

    @patch("main.billing_v1.CloudBillingClient")
    def test_disable_billing_error(self, mock_client_class):
        # Setup mock client to raise an exception
        mock_client = MagicMock()
        mock_client.update_project_billing_info.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client

        # Verify the exception is raised when calling the function
        with self.assertRaises(Exception) as context:
            main.disable_billing("test-project-123")

        self.assertEqual(str(context.exception), "API Error")


if __name__ == "__main__":
    unittest.main()

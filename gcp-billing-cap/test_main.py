import json
import base64
import sys
import os
import pytest
from unittest.mock import MagicMock, patch
from google.cloud import billing_v1

# Patch google.auth.default to prevent DefaultCredentialsError when main is imported
patch("google.auth.default", return_value=(MagicMock(), "mock-project")).start()

# Set environmental project ID so that main.PROJECT_ID is populated during import
os.environ["GCP_PROJECT"] = "test-project-123"

# Add directory to sys.path to resolve imports
sys.path.append("gcp-billing-cap")

import main  # noqa: E402


@pytest.fixture
def mock_disable_billing(mocker):
    # Mock the disable_billing function in main.py
    return mocker.patch("main.disable_billing")


@pytest.fixture
def mock_billing_client(mocker):
    # Mock the CloudBillingClient constructor in main.py
    mock_class = mocker.patch("main.billing_v1.CloudBillingClient")
    mock_instance = MagicMock()
    mock_class.return_value = mock_instance
    return mock_instance


def test_cap_billing_no_data():
    event = {}
    main.cap_billing(event, None)
    # Just verify it returns gracefully without raising errors


def test_cap_billing_invalid_json(mock_disable_billing):
    # base64 encoded invalid json
    encoded_data = base64.b64encode(b"invalid-json").decode("utf-8")
    event = {"data": encoded_data}

    with pytest.raises(json.JSONDecodeError):
        main.cap_billing(event, None)


def test_cap_billing_invalid_base64(mock_disable_billing):
    event = {"data": "invalid_base64_string_!@#$"}
    main.cap_billing(event, None)
    mock_disable_billing.assert_not_called()


def test_cap_billing_invalid_json(mock_disable_billing):
    # Valid base64, but invalid JSON (e.g., "not a json")
    encoded_data = base64.b64encode(b"not a json").decode("utf-8")
    event = {"data": encoded_data}
    main.cap_billing(event, None)
    mock_disable_billing.assert_not_called()


def test_cap_billing_under_budget(mock_disable_billing):
    data = {"costAmount": 50.0, "budgetAmount": 100.0}
    encoded_data = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    event = {"data": encoded_data}

    main.cap_billing(event, None)

    # disable_billing should not be called
    mock_disable_billing.assert_not_called()


def test_cap_billing_equal_budget(mock_disable_billing):
    data = {"costAmount": 100.0, "budgetAmount": 100.0}
    encoded_data = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    event = {"data": encoded_data}

    main.cap_billing(event, None)

    # disable_billing should be called
    mock_disable_billing.assert_called_once_with(main.PROJECT_ID)


def test_cap_billing_over_budget(mock_disable_billing):
    data = {"costAmount": 120.0, "budgetAmount": 100.0}
    encoded_data = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    event = {"data": encoded_data}

    main.cap_billing(event, None)

    # disable_billing should be called
    mock_disable_billing.assert_called_once_with(main.PROJECT_ID)


def test_cap_billing_missing_fields(mock_disable_billing):
    # Missing costAmount and budgetAmount in data (default to 0.0)
    data = {}
    encoded_data = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")
    event = {"data": encoded_data}

    main.cap_billing(event, None)

    # Since 0.0 >= 0.0 (both default to 0.0), it should disable billing
    mock_disable_billing.assert_called_once_with(main.PROJECT_ID)


def test_disable_billing_success(mock_billing_client):
    project_id = "test-project-123"

    mock_response = MagicMock()
    mock_billing_client.update_project_billing_info.return_value = mock_response

    main.disable_billing(project_id)

    # Ensure the client method was called with expected arguments
    mock_billing_client.update_project_billing_info.assert_called_once()

    # Extract arguments passed to the mock
    call_args = mock_billing_client.update_project_billing_info.call_args
    kwargs = call_args[1]

    assert kwargs["name"] == f"projects/{project_id}"
    assert isinstance(kwargs["project_billing_info"], billing_v1.ProjectBillingInfo)
    assert kwargs["project_billing_info"].billing_account_name == ""


def test_disable_billing_failure(mock_billing_client):
    project_id = "test-project-123"

    # Simulate an exception
    expected_error = Exception("API error")
    mock_billing_client.update_project_billing_info.side_effect = expected_error

    with pytest.raises(Exception) as exc_info:
        main.disable_billing(project_id)

    assert str(exc_info.value) == "API error"
    mock_billing_client.update_project_billing_info.assert_called_once()

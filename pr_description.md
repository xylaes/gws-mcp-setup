🎯 **What:** The testing gap addressed
The `disable_billing` function in `gcp-billing-cap/main.py` was previously untested. This function makes calls to the Google Cloud Billing API.

📊 **Coverage:** What scenarios are now tested
*   **Happy Path:** Verifies that `update_project_billing_info` is called with the correct project name and an empty billing account name.
*   **Error Condition:** Verifies that if the API call fails, the exception is raised properly.

✨ **Result:** The improvement in test coverage
The `disable_billing` function is now fully tested, making it safer to refactor in the future without causing unexpected regressions. In addition, the initialization of `CloudBillingClient` was moved from global scope to inside the `disable_billing` function scope, improving testability (and saving cold-start performance in production, as this function is rarely triggered).

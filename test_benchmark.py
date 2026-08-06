import unittest
from unittest.mock import patch
import io
import contextlib
import sys
import importlib

class TestBenchmark(unittest.TestCase):
    def test_benchmark_runs_and_outputs_correctly(self):
        """Test that importing/running benchmark.py executes process_payments and prints total time."""
        with patch('demo_bad_code.process_payments') as mock_process_payments, \
             patch('time.time') as mock_time, \
             contextlib.redirect_stdout(io.StringIO()) as mock_stdout:

            # Setup mocks
            mock_time.side_effect = [100.0, 102.5]  # Difference of 2.5 seconds
            mock_process_payments.return_value = 45.0

            # If benchmark was already imported, we reload it. Otherwise we import it.
            if 'benchmark' in sys.modules:
                importlib.reload(sys.modules['benchmark'])
            else:
                importlib.import_module('benchmark')

            # Assertions
            mock_process_payments.assert_called_once()
            called_args = mock_process_payments.call_args[0][0]
            self.assertEqual(len(called_args), 20)
            self.assertEqual(called_args[0], {'price': 0})
            self.assertEqual(called_args[-1], {'price': 19})

            # Check stdout output
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Total time: 2.5000s")

if __name__ == "__main__":
    unittest.main()

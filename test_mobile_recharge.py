"""
Unit tests for MobileRecharge class and validation functions.
Run with: python test_mobile_recharge.py
"""

import unittest
from app import MobileRecharge, validate_inputs, sanitize_mobile_number


class TestMobileRecharge(unittest.TestCase):

    def test_default_gst_calculation(self):
        # Base: 299, GST: 18% -> 53.82
        recharge = MobileRecharge(
            mobile_number="9876543210",
            plan_amount=299.0,
            plan_validity=28,
            data_per_day=1.5,
            talktime=0.0
        )
        self.assertEqual(recharge.gst_rate, 18.0)
        self.assertAlmostEqual(recharge.calculate_gst(), 53.82, places=2)
        self.assertAlmostEqual(recharge.calculate_total_amount(), 352.82, places=2)

    def test_custom_gst_rate(self):
        # Base: 500, GST: 10% -> 50, Total: 550
        recharge = MobileRecharge(
            mobile_number="9123456789",
            plan_amount=500.0,
            plan_validity=30,
            data_per_day=2.0,
            talktime=100.0,
            gst_rate=10.0
        )
        self.assertEqual(recharge.calculate_gst(), 50.0)
        self.assertEqual(recharge.calculate_total_amount(), 550.0)

    def test_display_plan_details(self):
        recharge = MobileRecharge(
            mobile_number="9988776655",
            plan_amount=1000.0,
            plan_validity=50,
            data_per_day=2.0,
            talktime=0.0
        )
        details = recharge.display_plan_details()
        self.assertEqual(details["mobile_number"], "9988776655")
        self.assertEqual(details["plan_amount"], 1000.0)
        self.assertEqual(details["gst_amount"], 180.0)
        self.assertEqual(details["total_amount"], 1180.0)
        self.assertEqual(details["total_data"], 100.0)  # 2.0 * 50
        self.assertEqual(details["cost_per_day"], 23.6)  # 1180 / 50
        self.assertEqual(details["talktime_label"], "Unlimited Calls")

    def test_sanitize_mobile_number(self):
        self.assertEqual(sanitize_mobile_number("+91 98765-43210"), "9876543210")
        self.assertEqual(sanitize_mobile_number("09876543210"), "9876543210")
        self.assertEqual(sanitize_mobile_number("9876543210"), "9876543210")

    def test_validate_inputs(self):
        # Valid input
        is_valid, errors = validate_inputs("9876543210", 299.0, 28, 1.5, 0.0)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

        # Invalid phone number (less than 10 digits)
        is_valid, errors = validate_inputs("12345", 299.0, 28, 1.5, 0.0)
        self.assertFalse(is_valid)

        # Invalid plan amount (0 or negative)
        is_valid, errors = validate_inputs("9876543210", 0.0, 28, 1.5, 0.0)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()

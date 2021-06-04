import unittest
from bmi_calculator.__main__ import bmi_details, bmi_type
import pandas as pd


class TestBMICalculator(unittest.TestCase):

    def setUp(self):
        input_json = [{"Gender": "Male", "HeightCm": 171, "WeightKg": 96}]
        self.df = pd.DataFrame(input_json)

    def test_bmi_type(self):
        result = bmi_type(18.4)
        self.assertEqual(result[0], "Underweight")

    def test_exception_bmi_type(self):
        try:
            bmi_type("23")
        except ValueError:
            self.assertRaises(ValueError)

    def test_bmi_details(self):
        result = bmi_details(self.df.iloc[0])
        self.assertEqual(result[0], 32.83)

    def test_exception_bmi_details(self):
        result = bmi_details(self.df)
        self.assertEqual(result[0], "")

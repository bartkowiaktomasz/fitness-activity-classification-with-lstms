"""
Script for Flask app unit testing.
Ignore warnings with:
python -W ignore test_analyzemyworkout.py

Coverage:
coverage run --source . --omit=test_data_collection.py,data_collection.py test_analyzemyworkout.py
"""

import unittest
import pexpect
import sys
sys.path.append("..")

from flask import Flask

import analyzemyworkout
from analyzemyworkout import app
from config import *

class TestAnalyzemyworkout(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(pexpect.exceptions.TIMEOUT):
            response = self.app.post('/', data={})

if __name__ == '__main__':
    unittest.main()

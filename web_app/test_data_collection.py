"""
Script for Flask app unit testing.
Ignore warnings with:
python -W ignore test_data_collection.py

Coverage:
coverage run --source . --omit=test_analyzemyworkout.py,analyzemyworkout.py test_data_collection.py
"""

import unittest
import sys
sys.path.append("..")

from flask import Flask

import data_collection
from data_collection import app
from config import *

class TestDataCollection(unittest.TestCase):
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

        with self.assertRaises(NameError):
            response = self.app.post('/', data={'activity': 'This activity does not exist'})

if __name__ == '__main__':
    unittest.main()

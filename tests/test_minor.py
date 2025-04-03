# -*- coding: utf-8 -*-
"""
* Unittest file that tests Minor functions.
? @LifelagCheats
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from main import WebRequestHandler

import requests
from halo import Halo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ? This will tests MINOR functions, that really don't matter
# TODO: add other functions for testing
sys.stdout.reconfigure(encoding='utf-8') # * Set utf encoding for windows.

class MinorUnitTests(unittest.TestCase):
    """ Class for the minor tests script. """
    def setUp(self):
        """Set up the WebRequestHandler instance once per test."""
        self.checker = WebRequestHandler()

    def test_normalizer(self):
        """ Test the website URL normalizer. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing normalizer... ')
        try:
            url = 'google.com'
            result = self.checker.normalize_url(url)

            self.assertEqual(result, 'http://google.com') # ! make sure the function returns the correct result
            spinner.succeed("Function worked as expected")

        except Exception as e:
            spinner.fail(f"Got error while testing: {str(e)}")

    @patch(
        'builtins.input', return_value='https://httpbin.org/get'
    )  # * Mock user input
    @patch('requests.get')
    def test_reseter(self, mock_get, mock_input):
        """ Tests the website reseter. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing website reseter... ')

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        try:
            self.checker.reset_website()
            self.assertEqual(self.checker.website, 'https://httpbin.org/get')
            spinner.succeed("Function worked as expected")

        except Exception as e:
            spinner.fail(f'Got error while testing: {str(e)}') # * clearer error handling

    def test_clear(self):
        """ Clear function testing. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing clear function')

        try:
            self.checker.clear_screen()
            spinner.succeed("Function worked as expected")

        except Exception as e:
            spinner.fail(f'Got error while testing: {str(e)}') 

if __name__ == '__main__':
    unittest.main()

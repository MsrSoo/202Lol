# -*- coding: utf-8 -*-
"""
Tests the website checker inside the main script individually.
@LifelagCheats
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from main import WebRequestHandler


from halo import Halo
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.stdout.reconfigure(encoding='utf-8') # * Set utf encoding for windows.

# ? Tests the website checker inside WebRequestHandler

class TestWebsiteChecker(unittest.TestCase):
    """ Class for the website checker. """
    def setUp(self):
        """Set up the WebRequestHandler instance once per test."""
        self.checker = WebRequestHandler()

    @patch('builtins.input', return_value='https://httpbin.org/get')
    @patch('requests.get')
    def test_checker_success(self, mock_get, mock_input):
        """ Tests the website checker for a successful reaction. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing website checker... ')

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        try:
            result = self.checker.check_website()
            self.assertTrue(result)
            spinner.succeed('Found no errors')

        except Exception as e:
            spinner.fail(f'Found error while testing: {str(e)}') # * clearer error handling

    @patch('builtins.input', return_value='https://nonexistentwebsite.com.org.net')
    @patch('requests.get', side_effect=requests.exceptions.ConnectionError)
    def test_checker_failure(self, mock_get, mock_input):
        """ Tests the website checker for failures. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing website checker...')

        try:
            result = self.checker.check_website()
            self.assertFalse(result)
            spinner.succeed('Found no errors')

        except Exception as e:
            spinner.fail(f'Found error while testing: {str(e)}') # * clearer error handling


if __name__ == '__main__':
    unittest.main()

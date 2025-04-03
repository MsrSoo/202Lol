# -*- coding: utf-8 -*-
"""
* Tests the poke function inside the main script individually.
? @LifelagCheats
"""
import unittest
from unittest.mock import patch, MagicMock
import socket
import os
import sys
from main import WebRequestHandler

import requests
from halo import Halo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.stdout.reconfigure(encoding='utf-8') # * Set utf encoding for windows.

# ? Tests the poke function inside the main script

class TestPokeWebsite(unittest.TestCase):
    """ Class for the testing poke function script. """
    @patch('requests.get')
    @patch('socket.gethostbyname')
    @patch('builtins.print')
    def test_poke_success(self, mock_print, mock_gethostbyname, mock_get):
        """ Tests how the poke function reacts to a successful interaction. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing poking function...')

        try:
            mocked = MagicMock()
            mocked.status_code = 200
            mocked.headers = {
                'Server': 'nginx',
                'X-Powered-By': 'PHP/7.4.3',
                'Set-Cookie': 'sessionid=testid',
            }
            mocked.cookies = [{'name': 'sessionid', 'value': 'testid'}]
            mock_get.return_value = mocked
            mock_gethostbyname.return_value = '192.39.14.1'

            url = 'https://httpbin.org'
            checker = WebRequestHandler()
            checker.poke_website(url)

            mock_print.assert_any_call("Website URL: https://httpbin.org")
            mock_print.assert_any_call("Hostname: httpbin.org")
            mock_print.assert_any_call("IP Address: 192.39.14.1")
            mock_print.assert_any_call("Server: nginx")
            mock_print.assert_any_call("X-Powered-By: PHP/7.4.3")

            spinner.succeed("Test was a success")

        except Exception as e:
            spinner.fail(f"Error during test: {str(e)}")
            raise

    @patch('requests.get')
    @patch('socket.gethostbyname')
    @patch('builtins.print')
    def test_poke_failure(self, mock_print, mock_gethostbyname, mock_get):
        """ Tests how the poke function reacts to a failure. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing poking failure results...')

        try:
            mock_get.side_effect = requests.exceptions.RequestException(
                "Request failed"
            )
            mock_gethostbyname.return_value = '192.39.14.1'

            url = 'https://nonexistentwebsite.com'
            checker = WebRequestHandler()
            checker.poke_website(url)

            spinner.succeed("Test was a success")

        except Exception as e:
            spinner.fail(f'Error during test: {str(e)}') # * clearer error handling

    @patch('requests.get')
    @patch('socket.gethostbyname')
    @patch('builtins.print')
    def test_poke_website_dns_error(self, mock_print, mock_gethostbyname, mock_get):
        """ Tests how the poke function reacts to a DNS error. """
        spinner = Halo(spinner='dots')
        spinner.start('Testing DNS errors...')
        try:
            mock_gethostbyname.side_effect = socket.gaierror("DNS resolution error")

            url = 'https://example.com'
            checker = WebRequestHandler()
            checker.poke_website(url)

            spinner.succeed("Test was a success")

        except Exception as e:
            spinner.fail(f'Error during test: {str(e)}')


if __name__ == '__main__':
    unittest.main() # * run the script

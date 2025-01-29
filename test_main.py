import pytest
import requests
import socket
from unittest.mock import patch, MagicMock
from main import normalize, poke_website, clear, torproxies, hproxies


@pytest.mark.parametrize("input_url,expected", [
    ("example.com", "http://example.com"),
    ("http://example.com", "http://example.com"),
    ("https://example.com", "https://example.com"),
    ("google.com", "http://google.com"),
])
def test_normalize(input_url, expected):
    assert normalize(input_url) == expected

@pytest.mark.parametrize("os_name,expected_command", [
    ("nt", "cls"),
    ("posix", "clear"),
])
def test_clear(os_name, expected_command):
    with patch('os.name', os_name):
        with patch('subprocess.run') as mock_run:
            clear()
            mock_run.assert_called_once_with([expected_command], shell=False)


def test_clear_subprocess_error():
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
        clear() 


def test_proxy_configurations():
    assert isinstance(torproxies, dict)
    assert isinstance(hproxies, dict)
    assert "http" in torproxies
    assert "https" in torproxies
    assert "http" in hproxies
    assert "https" in hproxies

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.headers = {
        "Server": "nginx",
        "X-Powered-By": "PHP/7.4.0",
        "Set-Cookie": "session=abc123"
    }
    mock.cookies = [MagicMock(name="sessionid", value="abc123")]
    mock.raw.version = "HTTP/1.1"
    return mock


def test_poke_website(mock_response):
    test_url = "http://example.com"
    
    with patch('requests.get', return_value=mock_response) as mock_get:
        with patch('socket.gethostbyname', return_value="93.184.216.34") as mock_socket:
            poke_website(test_url)
            
            # Verify the request was made
            mock_get.assert_called_once()
            mock_socket.assert_called_once()


def test_poke_website_connection_error():
    with patch('requests.get', side_effect=requests.exceptions.RequestException):
        poke_website("http://nonexistent.example.com")  


def test_poke_website_dns_error():
    with patch('requests.get', side_effect=socket.gaierror):
        poke_website("http://nonexistent.example.com")  


def test_logging_configuration():
    import logging
    root_logger = logging.getLogger()
    assert root_logger.level <= logging.DEBUG  
    

    has_file_handler = any(
        isinstance(handler, logging.FileHandler) 
        for handler in root_logger.handlers
    )
    assert has_file_handler  


def test_default_timeout():
    from main import timeout
    assert isinstance(timeout, int)
    assert timeout > 0  

if __name__ == "__main__":
    pytest.main(["-v"])

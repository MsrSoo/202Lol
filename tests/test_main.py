import pytest
import requests
from main import normalize, clear
import os
import subprocess
import time
import responses

@pytest.fixture
def test_website():
    return "httpbin.org"

def test_normalize_with_http():
    assert normalize("http://example.com") == "http://example.com"

def test_normalize_with_https():
    assert normalize("https://example.com") == "https://example.com"

def test_normalize_without_prefix():
    assert normalize("example.com") == "http://example.com"

def test_clear_linux(monkeypatch):
    monkeypatch.setattr(os, 'name', 'posix')
    with pytest.raises(subprocess.SubprocessError):
      clear()

def test_clear_windows(monkeypatch):
    monkeypatch.setattr(os, 'name', 'nt')
    with pytest.raises(subprocess.SubprocessError):
      clear()

def test_successful_get_request(monkeypatch, test_website, capsys):
    monkeypatch.setattr('builtins.input', lambda _: test_website)
    with pytest.raises(SystemExit):
        exec(open("main.py").read())
    captured = capsys.readouterr()
    assert "Website is valid, Proceeding" in captured.out
    response = requests.get(f"http://{test_website}/get", timeout=3)
    assert response.status_code == 200

def test_successful_post_request(monkeypatch, test_website):
    monkeypatch.setattr('builtins.input', lambda _: test_website)
    with pytest.raises(SystemExit):
          exec(open("main.py").read())
    response = requests.post(f"http://{test_website}/post", timeout=3, data={"key": "value"})
    assert response.status_code == 200
    assert response.json()["form"]["key"] == "value"

@responses.activate 
def test_request_timeout(monkeypatch, test_website, capsys):
    monkeypatch.setattr('builtins.input', lambda _: test_website)

    
    responses.add(responses.GET, f"http://{test_website}", body=b'{"error": "timeout"}', status=200, delay=5)


    with pytest.raises(SystemExit):
      exec(open("main.py").read())  

    captured = capsys.readouterr()
    assert "The request timed out." in captured.err

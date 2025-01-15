import pytest
import requests
from io import BytesIO

def normalize(website):   
    if not website.startswith(('http://', 'https://')):  
        website = 'http://' + website 
    return website 

def test_normalize_http():
    assert normalize("http://example.com") == "http://example.com"

def test_normalize_https():
    assert normalize("https://example.com") == "https://example.com"

def test_normalize_no_prefix():
    assert normalize("example.com") == "http://example.com"

def test_get_request(monkeypatch, requests_mock):
    monkeypatch.setattr('builtins.input', lambda _: "httpbin.org")
    requests_mock.get("http://httpbin.org", status_code=200, json={"url": "http://httpbin.org"})  
    monkeypatch.setattr('builtins.input', lambda _: "testpayload")
    monkeypatch.setattr('builtins.input', lambda _: "testvalue")
    monkeypatch.setattr('builtins.input', lambda _: "n")
    monkeypatch.setattr('builtins.input', lambda _: "1")
    monkeypatch.setattr('builtins.input', lambda _: "n")
    choices = ['post', 'get', 'file', 'exit', 'help', 'reset']
    user = 'get'
    if user not in choices:
        print("[red] Invalid command, please enter a valid one.")
    if user == "get":
        keyget = input("Name of the payload: ")
        variableget = input("Value of the payload: ")
        payloadget = {keyget: variableget}
        bisquit = input("Do you want to add cookies? (y/n) ").lower()
        if bisquit == 'n':
            numberget = int(input("Number of requests to do: "))
            for i in range(int(numberget)):
                rget = requests.get(website, params=payloadget, timeout=3)
            printresult_nocookies = input("Do you want to print the response and cookies? (y/n) ").lower()
            if printresult_nocookies == 'y':
                print(rget.text)
            elif printresult_nocookies == 'n':
                pass
            else:
                print("Invalid option")

def test_file_upload(monkeypatch, requests_mock):
    monkeypatch.setattr('builtins.input', lambda _: "httpbin.org/post") 
    monkeypatch.setattr('builtins.input', lambda _: "test_file.txt")  
    monkeypatch.setattr('builtins.input', lambda _: "test_file")  
    monkeypatch.setattr('builtins.input', lambda _: "post")  
    monkeypatch.setattr('builtins.input', lambda _: "n") 
    requests_mock.post("http://httpbin.org/post", status_code=200, json={"files": {"test_file": "File Content"}})
    mock_file = BytesIO(b"File Content")
    choices = ['post', 'get', 'file', 'exit', 'help', 'reset']
    user = 'file'
    if user not in choices:
        print( "[red] Invalid command, please enter a valid one.")
    if user == "file":
        typefile = "open" 
        filechoices = ['open', 'create']
        requestchoice = ['post', 'get']
        if typefile not in filechoices:
            print( "[red] Invalid choice")
        elif typefile == "open":
            openname = "test_file.txt" 
            filename = "test_file" 
            filecontent = {filename: (openname, mock_file)}  
            rqstype = "post" 
            if rqstype not in requestchoice:
                print("[red] Invalid choice")
            elif rqstype == "post":
                rfilepost = requests.post(website, files=filecontent, timeout=10)
                afileresult = input("Do you want to print the response and cookies? (y/n)").lower()
                if afileresult == 'y':
                    print(rfilepost.text)
                elif afileresult == 'n':
                    pass
                else:
                    print("[red] Invalid Option")

def test_invalid_command(capsys, monkeypatch):  
    monkeypatch.setattr('builtins.input', lambda _: "invalid_command")
    choices = ['post', 'get', 'file', 'exit', 'help', 'reset']
    user = input("\n>> ").lower()
    if user not in choices:
        print("[red] Invalid command, please enter a valid one.")
    captured = capsys.readouterr()
    assert "[red] Invalid command, please enter a valid one." in captured.out


def test_post_request(monkeypatch, requests_mock):
    monkeypatch.setattr('builtins.input', lambda _: "httpbin.org/post")
    requests_mock.post("http://httpbin.org/post", status_code=200, json={"url": "http://httpbin.org/post", "data": ""})  
    monkeypatch.setattr('builtins.input', lambda _: "testpayload")
    monkeypatch.setattr('builtins.input', lambda _: "testvalue")
    monkeypatch.setattr('builtins.input', lambda _: "n")
    monkeypatch.setattr('builtins.input', lambda _: "1")
    monkeypatch.setattr('builtins.input', lambda _: "n")


    choices = ['post', 'get', 'file', 'exit', 'help', 'reset']
    user = 'post'
    if user not in choices:
        print("[red] Invalid command, please enter a valid one.")

    if user == "post":  
        keypost = input("Name of the payload: ")  
        variablepost = input("Value of the payload: ")  
        payloadpost = {keypost: variablepost}  
        galleta = input("Do you want to add cookies? (y/n) ").lower()

        if galleta == 'n':
            numberpost = int(input("Number of requests to do: "))
            for i in range(int(numberpost)):
                rpost = requests.post(website, params=payloadpost, timeout=3)
            printresult_nogalleta = input("Do you want to print the response and cookies? (y/n) ").lower()
            if printresult_nogalleta == 'y':
                print(rpost.text)
            elif printresult_nogalleta == 'n':
                pass
            else:
                print("[red] Invalid Option")

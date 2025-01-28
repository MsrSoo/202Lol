import base64
import gc
import logging
import os
import socket
import subprocess
import time

import requests as rqs
import whois
from halo import Halo
from rich.console import Console
from tqdm import tqdm
from stem.control import Controller
from stem.connection import IncorrectPassword


def clear():
    try:
        if os.name == "nt":
            subprocess.run(["cls"], shell=False)
        else:
            subprocess.run(["clear"], shell=False)

    except subprocess.CalledProcessError as e:
        print(f"check50 failed: {e}")
        print(e.stderr)
    except subprocess.TimeoutExpired:
        print("Command timed out")


clear()

console = Console()

console.print(
    """[bold cyan]





    ██████╗  ██████╗ ██████╗ ██╗      ██████╗ ██╗
    ╚════██╗██╔═████╗╚════██╗██║     ██╔═══██╗██║
     █████╔╝██║██╔██║ █████╔╝██║     ██║   ██║██║
    ██╔═══╝ ████╔╝██║██╔═══╝ ██║     ██║   ██║██║
    ███████╗╚██████╔╝███████╗███████╗╚██████╔╝███████╗
    ╚══════╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚══════╝



                website requests handler
"""
)

webspin = Halo(text="Checking website...", spinner="dots")
payloadspin = Halo(text="Preparing payload...", spinner="dots")
jarspin = Halo(text="Building Jar...", spinner="dots")
spinner = Halo(text="", spinner="dots")

logging.basicConfig(
    filename="main.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
)

torproxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}

hproxies = {
    "http": "http://188.114.98.233:80",
    "https": "http://172.67.181.10:80",
}

default = hproxies

torenabled = False


def normalize(website):
    if not website.startswith(("http://", "https://")):
        website = "http://" + website
    return website


def poke_website(url):
    try:
        response = rqs.get(url, stream=True, timeout=timeout)

        hostname = url.split("//")[-1].split("/")[0]
        ip_address = socket.gethostbyname(hostname)

        print(f"Website URL: {url}")
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
        print("\nResponse Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        server_info = response.headers.get("Server", "Not Found")
        powered_by = response.headers.get("X-Powered-By", "Not Found")

        print("\nServer Info:")
        print(f"Server: {server_info}")
        print(f"X-Powered-By: {powered_by}")

        if "Set-Cookie" in response.headers:
            print("\nCookies Set by the Server:")
            for cookie in response.cookies:
                print(f"{cookie.name}: {cookie.value}")

        print("\nConnection details:")
        print(f"Protocol: {response.raw.version}")

        response.close()
    except rqs.exceptions.RequestException as e:
        console.print("[bold red] Error during request, please  consult log file.")
        logging.error({e})
    except socket.gaierror as e:
        console.print("[bold red]Error in DNS resolution, please consult log file.")
        logging.error({e})


def tor_enable():
    password = input("Tor password: ")
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=password)  # Replace with your Tor password
        controller.signal("NEWNYM")  # Request a new identity

    try:
        toresponse = rqs.get("http://check.torproject.org", proxies=default, timeout=10)
        if "Congratulations. This browser is configured to use Tor" in toresponse.text:
            console.print("[green] Traffic is routed through Tor!")
        else:
            console.print("[red] Traffic is NOT routed through Tor.")
    except IncorrectPassword as e:
        console.print("[bold red] Incorrect password.")
        logging.error({e})
    except Exception as e:
        console.print("[bold red] Got an unexpected error, please check log file.")
        logging.error({e})


def tor_disable():
    try:
        password = input("Tor password: ")
        with Controller.from_port(port=9051) as controller:
            try:
                controller.authenticate(password=password)
                controller.signal("SHUTDOWN")
                console.print("[green] Disabled tor traffic routing")
            except IncorrectPassword as e:
                console.print("[bold red] Incorrect password.")
                logging.error({e})
    except Exception as e:
        console.print("[bold red] Got unexpected error, please check log file")
        logging.error({e})


try:
    website = input("Website url: ").lower()
    website = normalize(website)
    timeout = 15
    r = rqs.get(website, timeout=timeout, proxies=default)
    webspin.start()
    time.sleep(4)
    response = r.status_code
    if response == 200:
        spinner.succeed("Website is valid, Proceeding")
        webspin.stop()
    else:
        spinner.fail("Error: Website could not be reached. Please enter a valid url")
        webspin.stop()
except KeyboardInterrupt:
    print("\nTerminated by user.")
except rqs.exceptions.ConnectionError as e:
    console.print(
        "[bold red] A connection error ocurred or server not reachable, please see log file"
    )
    logging.error({e})
except rqs.exceptions.Timeout:
    print("The request timed out.")
except rqs.exceptions.RequestException as e:
    console.print("[bold red] Exception error ocurred, please see log file.")
    logging.error({e})

while True:
    try:
        choices = [
            "post",
            "get",
            "file",
            "exit",
            "help",
            "reset",
            "whois",
            "proxies-socks",
            "proxies-http",
            "config-proxies" "poke",
            "timeout-config",
            "tor-enable",
            "tor-disable",
        ]
        user = input("\n>> ").lower()
        if user not in choices:
            console.print("[red] Invalid command, please enter a valid one.")

        if user == "get":
            keyget = input("Name of the payload: ")
            variableget = input("Value of the payload: ")
            payloadspin.start()
            payloadget = {keyget: variableget}
            time.sleep(5)
            payloadspin.stop()
            bisquit = input("Do you want to add cookies? (y/n) ").lower()

            if bisquit == "y":
                jarred = input("Do you want to use a jar? (y/n) ").lower()

                if jarred == "y":
                    jarget = rqs.cookies.RequestsCookieJar()
                    jarget_name = input("Enter the name of the cookie: ")
                    jarget_value = input("Enter the value of the cookie: ")
                    jarget_path = input(
                        "Enter the path of the website where the cookies will be: "
                    )
                    jarspin.start()
                    jarget.set(
                        jarget_name, jarget_value, domain=website, path=jarget_path
                    )
                    time.sleep(4)
                    jarspin.stop()
                    jargeturl = input("Enter the url: ")
                    cookienumber = int(input("Number of cookie requests to do: "))
                    console.print(f"[bold cyan] Sending requests...")
                    gc.disable()
                    for i in tqdm(range(int(cookienumber))):
                        jarequest = rqs.get(
                            jargeturl, cookies=jarget, timeout=timeout, proxies=default
                        )
                    gc.collect()
                    gc.enable()
                    printresult_jar = input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    if printresult_jar == "y":
                        print(jarequest.text)
                    elif printresult_jar == "n":
                        pass
                    else:
                        print("Invalid Option")

                elif jarred == "n":
                    numberget = int(input("Number of requests to do: "))
                    cookieget = input(
                        "Enter the name of the cookies you want to get after this: "
                    )
                    gc.disable()
                    console.print(f"[bold cyan] Sending requests...")
                    for i in tqdm(range(int(numberget))):
                        rget = rqs.get(
                            website, params=payloadget, timeout=timeout, proxies=default
                        )
                    gc.collect()
                    gc.enable()
                    printresult_nojar = input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    if printresult_nojar == "y":
                        print(rget.text)
                        print(rget.cookies[cookieget])
                    elif printresult_nojar == "n":
                        pass
                    else:
                        print("Invalid option")

            elif bisquit == "n":
                numberget = int(input("Number of requests to do: "))
                gc.disable()
                console.print(f"[bold cyan] Sending requests...")
                for i in tqdm(range(int(numberget))):
                    rget = rqs.get(
                        website, params=payloadget, timeout=timeout, proxies=default
                    )
                gc.collect()
                gc.enable()
                printresult_nocookies = input(
                    "Do you want to print the response and cookies? (y/n) "
                ).lower()
                if printresult_nocookies == "y":
                    print(rget.text)
                elif printresult_nocookies == "n":
                    pass
                else:
                    print("Invalid option")
            else:
                console.print("[italic red] Invalid option")

        elif user == "post":
            keypost = input("Name of the payload: ")
            variablepost = input("Value of the payload: ")
            time.sleep(2)
            payloadspin.start()
            time.sleep(4)
            payloadpost = {keypost: variablepost}
            payloadspin.stop()
            galleta = input("Do you want to add cookies? (y/n) ").lower()

            if galleta == "y":
                jarredo = input("Do you want to use a jar? (y/n) ").lower()
                if jarredo == "y":
                    jarpost = rqs.cookies.RequestsCookieJar()
                    jarpost_name = input("Enter the name of the cookie: ")
                    jarpost_value = input("Enter the value of the cookie: ")
                    jarpost_path = input(
                        "Enter the path of the website where the cookies will be: "
                    )
                    console.print("[yellow] Preparing the post Jar...")
                    jarspin.start()
                    time.sleep(4)
                    jarpost.set(
                        jarpost_name, jarpost_value, domain=website, path=jarpost_path
                    )
                    jarspin.stop()
                    jarposturl = input("Enter the url: ")
                    galletanumber = int(input("Number of cookie requests to do: "))
                    console.print(f"[bold cyan] Sending requests...")
                    gc.disable()
                    for i in tqdm(range(int(galletanumber))):
                        jarequestpost = rqs.post(
                            jarposturl, cookies=jarpost, timeout=timeout
                        )
                    gc.collect()
                    gc.enable()
                    printresult_jarredo = input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    if printresult_jarredo == "y":
                        print(jarequestpost.text)
                    elif printresult_jarredo == "n":
                        pass
                    else:
                        console.print("[red] Invalid Option")

                elif jarredo == "n":
                    numberpost = int(input("Number of requests to do: "))
                    cookiepost = input(
                        "Enter the name of the cookies you want to get after this: "
                    )
                    time.sleep(1)
                    console.print(f"[bold cyan] Sending requests...")
                    gc.disable()
                    for i in tqdm(range(int(numberpost))):
                        rpost = rqs.post(
                            website,
                            params=payloadpost,
                            timeout=timeout,
                            proxies=default,
                        )
                    gc.collect()
                    gc.enable()
                    printresult_nojarredo = input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    if printresult_nojarredo == "y":
                        print(rpost.text)
                        print(rpost.cookies[cookiepost])
                    elif printresult_nojarredo == "n":
                        pass
                    else:
                        console.print("[red] Invalid Option")

            elif galleta == "n":
                numberpost = int(input("Number of requests to do: "))
                console.print(f"[bold cyan] Sending requests...")
                gc.disable()
                for i in tqdm(range(int(numberpost))):
                    rpost = rqs.post(
                        website, params=payloadpost, timeout=timeout, proxies=default
                    )
                gc.collect()
                gc.enable()
                printresult_nogalleta = input(
                    "Do you want to print the response and cookies? (y/n) "
                ).lower()
                if printresult_nogalleta == "y":
                    print(rpost.text)
                elif printresult_nogalleta == "n":
                    pass
                else:
                    console.print("[red] Invalid Option")
            else:
                console.print("[red] Invalid option")

        elif user == "file":
            typefile = input("Do you want to open a file or create a string? ")
            filechoices = ["open", "create"]
            requestchoice = ["post", "get"]
            if typefile not in filechoices:
                console.print("[red] Invalid choice")
            elif typefile == "open":
                openname = input("Name of the file with extension to open: ")
                filename = input("Enter a simple file name: ")

                spinner.start("Preparing the payload's content...")
                filecontent = {filename: open(openname, "rb")}
                time.sleep(2)
                spinner.stop()
                rqstype = input("Type of request: ")
                if rqstype not in requestchoice:
                    console.print("[red] Invalid choice")
                elif rqstype == "post":
                    spinner.start("Preparing payload...")
                    rfilepost = rqs.post(
                        website, files=filecontent, timeout=timeout, proxies=default
                    )
                    time.sleep(1.2)
                    spinner.stop()
                    afileresult = input(
                        "Do you want to print the response and cookies? (y/n)"
                    ).lower()
                    if afileresult == "y":
                        print(rfilepost.text)
                    elif afileresult == "n":
                        pass
                    else:
                        console.print("[red] Invalid Option")
                elif rqstype == "get":
                    spinner.start("Preparing payload...")
                    rfileget = rqs.get(
                        website, files=filecontent, timeout=timeout, proxies=default
                    )
                    time.sleep(1.2)
                    spinner.stop()
                    bfileresult = input(
                        "Do you want to print the response and cookies? (y/n)"
                    ).lower()
                    if bfileresult == "y":
                        print(rfileget.text)
                    elif bfileresult == "n":
                        pass
                    else:
                        console.print("[red] Invalid Option")

            elif typefile == "create":
                method = input(
                    "Do you want an auto generated file (a) or a custom string (b)? "
                )
                if method == "a":
                    num_lines = int(
                        input("Enter the number of lines of gibberish you want: ")
                    )
                    autofilename = input(
                        "Enter the name of the output text file (with .txt extension): "
                    )
                    headername = input(
                        "Enter a simple name for the payload header name: "
                    )
                    numreq = int(
                        input("Enter the number of times you want to do the request: ")
                    )

                    gibberish_lines = []
                    console.print("[blue] Preparing payload...")
                    for _ in tqdm(range(int(num_lines)), desc="Generating Lines...  "):
                        random_bytes = os.urandom(32)
                        base64_line = base64.b64encode(random_bytes).decode("utf-8")
                        gibberish_lines.append(base64_line)

                    time.sleep(2)
                    with open(autofilename, "w", encoding="utf-8") as f:
                        for line in tqdm(gibberish_lines, desc="Writing Lines...  "):
                            f.write(line + "\n")

                    time.sleep(1)
                    console.print(
                        f"[bold green] File generated and saved to {autofilename}"
                    )

                    autowritetype = input("Type of requests: ")
                    if autowritetype not in requestchoice:
                        console.print("[red] Invalid choice")
                    elif autowritetype == "post":
                        autofilecontent = {headername: open(autofilename, "rb")}
                        console.print(f"[italic blue] Sending payload...")
                        time.sleep(1)
                        for i in tqdm(range(int(numreq))):
                            autowritepost = rqs.post(
                                website,
                                files=autofilecontent,
                                timeout=timeout,
                                proxies=default,
                            )
                        time.sleep(0.5)
                        ffileresult = input(
                            "Do you want to print the response and cookies? (y/n) "
                        ).lower()
                        if ffileresult == "y":
                            print(autowritepost)
                        elif ffileresult == "n":
                            pass
                        else:
                            console.print("[red] Invalid Option")
                    elif autowritetype == "get":
                        console.print(f"[bold cyan] Sending payload...")
                        for i in tqdm(range(int(numreq))):
                            autowriteget = rqs.get(
                                website,
                                files=autofilecontent,
                                timeout=timeout,
                                proxies=default,
                            )
                        ffileresult = input(
                            "Do you want to print the response and cookies? (y/n) "
                        ).lower()
                        if ffileresult == "y":
                            print(autowriteget)
                        elif ffileresult == "n":
                            pass
                        else:
                            console.print("[red] Invalid Option")

                elif method == "b":
                    writename = input("File name with extension: ")
                    writestring = input("String for file: ")
                    writefilename = input("Enter a simple file name: ")
                    spinner.start("Preparing the file contents...")
                    time.sleep(2.4)
                    spinner.stop()
                    writecontent = {writefilename: (writename, writestring)}
                    writetype = input("Type of requests: ")
                    if writetype not in requestchoice:
                        console.print("[red] Invalid choice")
                    elif writetype == "post":
                        writepost = rqs.post(
                            website,
                            files=writecontent,
                            timeout=timeout,
                            proxies=default,
                        )
                        cfileresult = input(
                            "Do you want to print the response and cookies? (y/n)"
                        ).lower()
                        if cfileresult == "y":
                            print(writepost)
                        elif cfileresult == "n":
                            pass
                        else:
                            console.print("[red]Invalid Option")
                    elif writetype == "get":
                        writeget = rqs.get(
                            website,
                            files=writecontent,
                            timeout=timeout,
                            proxies=default,
                        )
                        dfileresult = input(
                            "Do you want to print the response and cookies? (y/n)"
                        ).lower()
                        if dfileresult == "y":
                            print(writeget)
                        elif dfileresult == "n":
                            pass
                        else:
                            console.print("[red] Invalid Option")
                else:
                    console.print("[red] Invalid option")

        elif user == "whois":
            try:
                whoisweb = input("Enter website to be searched: ")
                whoisweb = normalize(whoisweb)
                info = whois.whois(whoisweb)
                print(info)
            except whois.parser.PywhoisError:
                print("Invalid website or server not reachable.")

        elif user == "reset":
            websiteagain = input("Enter new website: ")
            websiteagain = normalize(websiteagain)
            rg = rqs.get(websiteagain, timeout=timeout, proxies=default)
            webspin.start()
            time.sleep(4)
            response = r.status_code
            if response == 200:
                spinner.succeed("Website is valid, Proceeding")
                website = websiteagain
                webspin.stop()
            else:
                spinner.fail(
                    "Error: Website could not be reached. Please enter a valid url"
                )
                webspin.stop()

        elif user == "poke":
            poke_website(website)

        elif user == "proxies-socks":
            newsocks1 = input("Enter the new http socks proxy: ")
            newsocks2 = input("Enter the new https socks proxy: ")

            if newsocks1:
                torproxies["http"] = newsocks1
            elif newsocks2:
                torproxies["https"] = newsocks2

        elif user == "proxies-http":
            newhttp = input("Enter the http proxy: ")
            newhttps = input("Enter the https proxy: ")

            if newhttp:
                hproxies["http"] = newhttp
            elif newhttps:
                hproxies["https"] = newhttps

        elif user == "tor-enable":
            try:
                if torenabled == True:
                    console.print("[yellow] Tor traffic routing is already enabled!")
                else:
                    tor_enable()
                    torenabled = True
            except Exception as e:
                console.print(
                    "[bold red] Got an unexpected error, please check log file."
                )
                logging.error({e})
        elif user == "tor-disable":
            try:
                if torenabled == False:
                    console.print("[yellow] Tor traffic routing is already disabled!")
                else:
                    tor_disable()
                    torenabled = False
            except Exception as e:
                console.print(
                    "[bold red] Got an unexpected error, please check log file."
                )
                logging.error({e})
        elif user == "config-proxies":
            try:
                if default == hproxies:
                    default = torproxies
                    console.print("[green] configured the proxy to use successfully")
                else:
                    default = torproxies
                    console.print("[green] configured the proxy to use successfully")
            except Exception as e:
                console.print(
                    "[bold red] Got an unexpected error, please check log file."
                )
                logging.error({e})

        elif user == "timeout-config":
            newtime = int(input("Enter new timeout: "))
            timeout = newtime

        elif user == "help":
            console.print(
                """[bold green]
            
            ======= Help Manual =======


            file - send a file as a request
            get - send a request of type get; you can choose between adding cookies or not
            post - send a request of type post; you can choose between adding cookies or not
            reset - define a new website
            whois - fetch whois information
            poke - make an incomplete request that recons info
            timeout-config - customize your timeout time in seconds
            tor-enable - Enable tor traffic routing
            tor-disable - Disable tor traffic routing
            proxies-socks - Configure your socks proxies
            proxies-http - Configure your http proxies
            config-proxies - Define which proxy to use, http or SOCKS5
            exit - end the session
            help - show this message

            ===========================
            
            """
            )

        elif user == "exit":
            console.print("[bold yellow] Exiting...")
            break

    except KeyboardInterrupt:
        console.print("[bold yellow] Script terminated by user")
        break

    except rqs.exceptions.ConnectionError as e:
        console.print(
            "[bold red] A connection error ocurred or server not reachable, please see log file."
        )
        logging.error({e})
    except rqs.exceptions.Timeout:
        print("The request timed out.")
    except rqs.exceptions.RequestException as e:
        console.print("[bold red] Exception error ocurred, please see log file.")
        logging.error({e})

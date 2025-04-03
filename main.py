# -*- coding: utf-8 -*-
import base64
import gc
import logging
import os
import random
import socket
import subprocess
import time
import sys
from typing import Dict, Optional, Union

import requests
from halo import Halo # ? Halo because it looks cool
from rich.console import Console
from stem.connection import IncorrectPassword
from stem.control import Controller
from tqdm import tqdm # ? Tqdm for more "precise" info (i just want you to think the loading is going to end soon).
sys.stdout.reconfigure(encoding='utf-8')

class WebRequestHandler:
    def __init__(self):
        self.console = Console()
        self.website = ""
        self.timeout = 15
        self.torenabled = False

        # * Initialize variables
        self.torproxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
        }
        self.hproxies = {
            "http": "http://65.1.244.232:1080",
            "https": "http://65.1.244.232:1080",
        }
        self.default = self.hproxies

        # Configure logging
        logging.basicConfig(
            filename="main.log",
            encoding="utf-8",
            level=logging.DEBUG,
            format="%(levelname)s: %(message)s",
        )

        # * Initialize spinners
        self.webspin = Halo(text="Checking website...", spinner="dots")
        self.payloadspin = Halo(text="Preparing payload...", spinner="dots")
        self.jarspin = Halo(text="Building Jar...", spinner="dots")
        self.spinner = Halo(text="", spinner="dots")

        # * Display startup banner
        self.display_banner()

    def display_banner(self):
        """Display the ASCII art banner with a random color and quote."""
        self.clear_screen()

        color_palettes = {
            "blue": ["#4c4cff", "#6666ff", "#8080ff", "#9999ff"],
            "cyan": ["#66ffff", "#80ffff", "#99ffff", "#b3ffff"],
        }

        quotes = [
            "Talk is cheap. Show me the code.",
            "The best way to predict the future is to implement it.",
            "There is only one way to eat an elephant: a byte at a time.",
            "It's not a bug – it's an undocumented feature.",
            "Code is like humor. When you have to explain it, its bad.",
            "Programs must be written for people to read, and only incidentally for machines to execute.",
        ]

        selected_color = random.choice(list(color_palettes.keys()))
        shades = color_palettes[selected_color]
        quote = random.choice(quotes)

        ascii_text = f"""
 [{shades[0]}]██████╗  ██████╗ ██████╗ ██╗      ██████╗ ██╗
 [{shades[1]}]╚════██╗██╔═████╗╚════██╗██║     ██╔═══██╗██║      
  [{shades[2]}]█████╔╝██║██╔██║ █████╔╝██║     ██║   ██║██║    
 [{shades[3]}]██╔═══╝ ████╔╝██║██╔═══╝ ██║     ██║   ██║██║    
 [{shades[0]}]███████╗╚██████╔╝███████╗███████╗╚██████╔╝███████╗    
 [{shades[1]}]╚══════╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚══════╝
 
 [{shades[2]}]Website Request Handler[/]             Made by LifelagCheats
 [{shades[3]}]{quote}[/]
        """
        self.console.print(ascii_text)

    def clear_screen(self):
        """Clear the terminal screen."""
        try:
            if os.name == "nt":
                subprocess.run([r"C:\Windows\System32\cmd.exe", "/c", "cls"], shell=False)
            else:
                subprocess.run(["/bin/bash", "-c", "clear"], shell=False)
        except subprocess.CalledProcessError as e:
            print(f"Clear screen failed: {e}")
            print(e.stderr)
        except subprocess.TimeoutExpired:
            print("Command timed out")

    def normalize_url(self, url: str) -> str:
        """Add http:// prefix if missing"""
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return url

    def poke_website(self, url: str):
        """Gather information about the website without making a full request."""
        try:
            response = requests.get(
                url, stream=True, timeout=self.timeout, proxies=self.default
            )

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

            print("\nConnection details:")
            print(f"Protocol: {response.raw.version}")

            response.close()
        except requests.exceptions.RequestException as e:
            self.console.print(
                "[bold red] Error during request, please consult log file."
            )
            logging.error(str(e))
        except socket.gaierror as e:
            self.console.print(
                "[bold red]Error in DNS resolution, please consult log file."
            )
            logging.error(str(e))

    def tor_enable(self):
        """Enable Tor routing for requests."""
        try:
            password = input("Tor password: ")
            with Controller.from_port(port=9051) as controller:
                controller.authenticate(password=password)
                controller.signal("NEWNYM")  # * Request a new identity

            tor_response = requests.get(
                "http://check.torproject.org", proxies=self.default, timeout=10 # * Check to see if tor has been applied successfully
            )
            if (
                "Congratulations. This browser is configured to use Tor"
                in tor_response.text
            ):
                self.console.print("[green] Traffic is routed through Tor!")
                self.torenabled = True
            else:
                self.console.print("[red] Traffic is NOT routed through Tor.")
        except IncorrectPassword:
            self.console.print("[bold red] Incorrect password.")
        except Exception as e:
            self.console.print(
                "[bold red] Got an unexpected error, please check log file."
            )
            logging.error(str(e))

    def tor_disable(self):
        """Disable Tor routing for requests."""
        try:
            password = input("Tor password: ")
            with Controller.from_port(port=9051) as controller:
                try:
                    controller.authenticate(password=password)
                    controller.signal("SHUTDOWN")
                    self.console.print("[green] Disabled tor traffic routing")
                    self.torenabled = False
                except IncorrectPassword:
                    self.console.print("[bold red] Incorrect password.")
        except Exception as e:
            self.console.print("[bold red] Got unexpected error, please check log file")
            logging.error(str(e))

    def check_website(self):
        """Validate that the website is accessible."""
        try:
            url = input("Website url: ").lower()
            url = self.normalize_url(url)

            self.webspin.start()
            r = requests.get(url, timeout=self.timeout, proxies=self.default)

            response = r.status_code
            if response == 200: 
                self.spinner.succeed("Website is valid, Proceeding")
                self.website = url
            else:
                self.spinner.fail(
                    "Error: Website could not be reached. Please enter a valid url"
                )
                logging.debug(str(response))
                return False

            self.webspin.stop()
            return True
        except KeyboardInterrupt:
            print("\nTerminated by user.")
            return False
        except requests.exceptions.ConnectionError as e:
            self.console.print(
                "[bold red] A connection error occurred or server not reachable, please see log file"
            )
            logging.error(str(e))
            return False
        except requests.exceptions.Timeout:
            print("The request timed out.")
            return False
        except requests.exceptions.RequestException as e:
            self.console.print(
                "[bold red] Exception error occurred, please see log file."
            )
            logging.error(str(e))
            return False

    def send_get_request(self):
        """Handle GET requests with various options."""
        key = input("Name of the payload: ")
        value = input("Value of the payload: ")

        self.payloadspin.start()
        payload = {key: value}
        self.payloadspin.stop()

        use_cookies = input("Do you want to add cookies? (y/n) ").lower() == "y"

        if use_cookies:
            use_jar = input("Do you want to use a jar? (y/n) ").lower() == "y"

            if use_jar:
                jar = requests.cookies.RequestsCookieJar()
                jar_name = input("Enter the name of the cookie: ")
                jar_value = input("Enter the value of the cookie: ")
                jar_path = input(
                    "Enter the path of the website where the cookies will be: "
                )

                self.jarspin.start()
                jar.set(
                    jar_name,
                    jar_value,
                    domain=self.website.split("//")[-1].split("/")[0], # ? funny solution to only get the website's name without the http before it
                    path=jar_path,
                )
                self.jarspin.stop()

                jar_url = input("Enter the url: ")
                cookie_count = int(input("Number of cookie requests to do: "))

                self.console.print(f"[bold cyan] Sending requests...")
                gc.disable()
                for _ in tqdm(range(cookie_count)):
                    jar_request = requests.get(
                        jar_url, cookies=jar, timeout=self.timeout, proxies=self.default
                    )
                gc.collect()
                gc.enable()

                if (
                    input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    == "y"
                ):
                    print(jar_request.text)
            else:
                # * Non-jar cookie request
                req_count = int(input("Number of requests to do: "))
                cookie_name = input(
                    "Enter the name of the cookies you want to get after this: "
                )

                gc.disable()
                self.console.print(f"[bold cyan] Sending requests...")
                for _ in tqdm(range(req_count)):
                    r_get = requests.get(
                        self.website,
                        params=payload,
                        timeout=self.timeout,
                        proxies=self.default,
                    )
                gc.collect()
                gc.enable()

                if (
                    input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    == "y"
                ):
                    print(r_get.text)
                    if cookie_name in r_get.cookies:
                        print(r_get.cookies[cookie_name])
                    else:
                        print("Cookie not found")
        else:
            # * Basic GET request without cookies
            req_count = int(input("Number of requests to do: "))

            gc.disable()
            self.console.print(f"[bold cyan] Sending requests...")
            for _ in tqdm(range(req_count)):
                r_get = requests.get(
                    self.website,
                    params=payload,
                    timeout=self.timeout,
                    proxies=self.default,
                )
            gc.collect()
            gc.enable()

            if (
                input("Do you want to print the response and cookies? (y/n) ").lower()
                == "y"
            ):
                print(r_get.text)

    def send_post_request(self):
        """Handle POST requests with various options."""
        key = input("Name of the payload: ")
        value = input("Value of the payload: ")

        self.payloadspin.start()
        payload = {key: value}
        self.payloadspin.stop()

        use_cookies = input("Do you want to add cookies? (y/n) ").lower() == "y"

        if use_cookies:
            use_jar = input("Do you want to use a jar? (y/n) ").lower() == "y"

            if use_jar:
                jar = requests.cookies.RequestsCookieJar()
                jar_name = input("Enter the name of the cookie: ")
                jar_value = input("Enter the value of the cookie: ")
                jar_path = input(
                    "Enter the path of the website where the cookies will be: "
                )

                self.jarspin.start()
                jar.set(
                    jar_name,
                    jar_value,
                    domain=self.website.split("//")[-1].split("/")[0],
                    path=jar_path,
                )
                self.jarspin.stop()

                jar_url = input("Enter the url: ")
                cookie_count = int(input("Number of cookie requests to do: "))

                self.console.print(f"[bold cyan] Sending requests...")
                gc.disable()
                for _ in tqdm(range(cookie_count)):
                    jar_request = requests.post(
                        jar_url, cookies=jar, timeout=self.timeout, proxies=self.default
                    )
                gc.collect()
                gc.enable()

                if (
                    input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    == "y"
                ):
                    print(jar_request.text)
            else:
                # * Non-jar cookie request
                req_count = int(input("Number of requests to do: "))
                cookie_name = input(
                    "Enter the name of the cookies you want to get after this: "
                )

                gc.disable()
                self.console.print(f"[bold cyan] Sending requests...") # ? I use cyan because it looks cool btw.
                for _ in tqdm(range(req_count)):
                    r_post = requests.post(
                        self.website,
                        json=payload,
                        timeout=self.timeout,
                        proxies=self.default,
                    )
                gc.collect()
                gc.enable()

                if (
                    input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    == "y"
                ):
                    print(r_post.text)
                    if cookie_name in r_post.cookies: # * make sure the cookies are in the response
                        print(r_post.cookies[cookie_name]) 
                    else:
                        print("Cookie not found")
        else:
            # Basic POST request without cookies
            req_count = int(input("Number of requests to do: "))

            gc.disable()
            self.console.print(f"[bold cyan] Sending requests...")
            for _ in tqdm(range(req_count)):
                r_post = requests.post(
                    self.website,
                    json=payload,
                    timeout=self.timeout,
                    proxies=self.default,
                )
            gc.collect()
            gc.enable()

            if (
                input("Do you want to print the response and cookies? (y/n) ").lower()
                == "y"
            ):
                print(r_post.text)

    def handle_file_request(self):
        """Handle requests with file uploads."""
        file_type = input(
            "Do you want to open a file or create a string? (open/create): "
        )

        if file_type not in ["open", "create"]:
            self.console.print("[red] Invalid choice")
            return

        if file_type == "open":
            file_path = input("Name of the file with extension to open: ")
            field_name = input("Enter a simple file name: ")

            self.spinner.start("Preparing the payload's content...")
            file_content = {field_name: open(file_path, "rb")}
            time.sleep(1)
            self.spinner.stop()

            req_type = input("Type of request (post/get): ")

            if req_type not in ["post", "get"]:
                self.console.print("[red] Invalid choice")
                return

            self.spinner.start("Preparing payload...")
            if req_type == "post":
                response = requests.post(
                    self.website,
                    files=file_content,
                    timeout=self.timeout,
                    proxies=self.default,
                )
            else:  # GET
                response = requests.get(
                    self.website,
                    files=file_content,
                    timeout=self.timeout,
                    proxies=self.default,
                )

            self.spinner.stop()

            if (
                input("Do you want to print the response and cookies? (y/n)").lower()
                == "y"
            ):
                print(response.text)

        elif file_type == "create":
            method = input(
                "Do you want an auto generated file (a) or a custom string (b)? "
            )

            if method == "a":
                # ? I decided for an auto generated file of gibberish base64 because it is just a perfect payload. 
                # ? Don't enter too much or your pc might crash.
                num_lines = int(
                    input("Enter the number of lines of gibberish you want: ")
                )
                output_file = input(
                    "Enter the name of the output text file (with .txt extension): "
                )
                header_name = input("Enter a simple name for the payload header name: ")
                req_count = int(
                    input("Enter the number of times you want to do the request: ")
                )

                gibberish_lines = []
                self.console.print("[blue] Preparing payload...")

                for _ in tqdm(range(num_lines), desc="Generating Lines...  "):
                    random_bytes = os.urandom(32)
                    base64_line = base64.b64encode(random_bytes).decode("utf-8")
                    gibberish_lines.append(base64_line)

                with open(output_file, "w", encoding="utf-8") as f:
                    for line in tqdm(gibberish_lines, desc="Writing Lines...  "): # * gotta save it so we can use it according to the requests docs.
                        f.write(line + "\n")

                self.console.print(
                    f"[bold green] File generated and saved to {output_file}"
                )

                req_type = input("Type of requests (post/get): ")

                if req_type not in ["post", "get"]:
                    self.console.print("[red] Invalid choice")
                    return

                file_content = {header_name: open(output_file, "rb")}
                self.console.print(f"[italic blue] Sending payload...")

                if req_type == "post":
                    for _ in tqdm(range(req_count)):
                        response = requests.post(
                            self.website,
                            files=file_content,
                            timeout=self.timeout,
                            proxies=self.default,
                        )
                else:  # get
                    for _ in tqdm(range(req_count)):
                        response = requests.get(
                            self.website,
                            files=file_content,
                            timeout=self.timeout,
                            proxies=self.default,
                        )

                if (
                    input(
                        "Do you want to print the response and cookies? (y/n) "
                    ).lower()
                    == "y"
                ):
                    print(response.text)

            elif method == "b":
                # Custom string file
                file_name = input("File name with extension: ")
                file_string = input("String for file: ")
                field_name = input("Enter a simple file name: ")

                self.spinner.start("Preparing the file contents...")
                time.sleep(1)
                self.spinner.stop()

                file_content = {field_name: (file_name, file_string)}
                req_type = input("Type of requests (post/get): ")

                if req_type not in ["post", "get"]:
                    self.console.print("[red] Invalid choice")
                    return

                if req_type == "post":
                    response = requests.post(
                        self.website,
                        files=file_content,
                        timeout=self.timeout,
                        proxies=self.default,
                    )
                else:  # get
                    response = requests.get(
                        self.website,
                        files=file_content,
                        timeout=self.timeout,
                        proxies=self.default,
                    )

                if (
                    input(
                        "Do you want to print the response and cookies? (y/n)"
                    ).lower()
                    == "y"
                ):
                    print(response.text)
            else:
                self.console.print("[red] Invalid option")

    def reset_website(self):
        """Change the target website."""
        new_website = input("Enter new website: ")
        new_website = self.normalize_url(new_website)

        self.webspin.start()
        try:
            response = requests.get(
                new_website, timeout=self.timeout, proxies=self.default
            )
            time.sleep(1)

            if response.status_code == 200:
                self.spinner.succeed("Website is valid, Proceeding")
                self.website = new_website
            else:
                self.spinner.fail(
                    "Error: Website could not be reached. Please enter a valid url"
                )
        except requests.exceptions.RequestException:
            self.spinner.fail(
                "Error: Website could not be reached. Please enter a valid url"
            )

        self.webspin.stop()

    def update_socks_proxies(self):
        """Update SOCKS proxy settings."""
        http_proxy = input("Enter the new http socks proxy: ")
        https_proxy = input("Enter the new https socks proxy: ")

        if http_proxy:
            self.torproxies["http"] = http_proxy

        if https_proxy:
            self.torproxies["https"] = https_proxy

        self.console.print("[green] SOCKS proxies updated successfully")

    def update_http_proxies(self):
        """Update HTTP proxy settings."""
        http_proxy = input("Enter the http proxy: ")
        https_proxy = input("Enter the https proxy: ")

        if http_proxy:
            self.hproxies["http"] = http_proxy

        if https_proxy:
            self.hproxies["https"] = https_proxy

        self.console.print("[green] HTTP proxies updated successfully")

    def configure_proxies(self):
        """Toggle between HTTP and SOCKS proxy configurations."""
        try:
            if self.default == self.hproxies:
                self.default = self.torproxies
                self.console.print(
                    "[green] Configured the proxy to use tor socks successfully"
                )
            else:
                self.default = self.hproxies
                self.console.print(
                    "[green] Configured the proxy to use http proxies successfully"
                )
        except Exception as e:
            self.console.print(
                "[bold red] Got an unexpected error, please check log file."
            )
            logging.error(str(e))

    def update_timeout(self):
        """Change the timeout value for requests."""
        new_timeout = int(input("Enter new timeout (seconds): "))
        self.timeout = new_timeout
        self.console.print(f"[green] Timeout updated to {new_timeout} seconds")

    def show_help(self):
        """Display help information."""
        self.console.print(
            """[bold green]
            ======= Help Manual =======
   
            file - send a file as a request
            get - send a request of type get; you can choose between adding cookies or not
            post - send a request of type post; you can choose between adding cookies or not
            reset - define a new website
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

    def run(self):
        """Main program loop."""
        if not self.check_website():
            return

        while True:
            try:
                commands = {
                    "post": self.send_post_request,
                    "get": self.send_get_request,
                    "file": self.handle_file_request,
                    "reset": self.reset_website,
                    "poke": lambda: self.poke_website(self.website), # * because it is a standalone function that needs a direct parameter
                    "proxies-socks": self.update_socks_proxies,
                    "proxies-http": self.update_http_proxies,
                    "config-proxies": self.configure_proxies,
                    "timeout-config": self.update_timeout,
                    "tor-enable": self.tor_enable,
                    "tor-disable": self.tor_disable,
                    "help": self.show_help,
                    "exit": lambda: "exit",
                }

                user_input = input("\n>> ").lower()

                if user_input in commands:
                    result = commands[user_input]()
                    if result == "exit":
                        self.console.print("[bold yellow] Exiting...")
                        break
                else:
                    self.console.print(
                        "[red] Invalid command, please enter a valid one."
                    )

            except KeyboardInterrupt:
                self.console.print("[bold yellow] Script terminated by user")
                break
            except requests.exceptions.ConnectionError as e:
                self.console.print(
                    "[bold red] A connection error occurred or server not reachable, please see log file."
                )
                logging.error(str(e))
            except requests.exceptions.Timeout:
                print("The request timed out.")
            except requests.exceptions.RequestException as e:
                self.console.print(
                    "[bold red] Exception error occurred, please see log file."
                )
                logging.error(str(e))
            except Exception as e:
                self.console.print(
                    "[bold red] Unexpected error occurred, please see log file."
                )
                logging.error(str(e))


if __name__ == "__main__":
    handler = WebRequestHandler()
    handler.run()

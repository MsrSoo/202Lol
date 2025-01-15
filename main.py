import requests as rqs
from rich.console import Console
from tqdm import tqdm
import time
from halo import Halo
import subprocess
import base64
import os

def clear():
    try:
        if os.name == 'nt':
            subprocess.run(['cls'], shell=False)
        else:
            subprocess.run(['clear'], shell=False)

    except subprocess.CalledProcessError as e:
        print(f"check50 failed: {e}")
        print(e.stderr)        
    except subprocess.TimeoutExpired:
        print("Command timed out")

clear()

console = Console()

console.print("""[bold cyan]
    




    ██████╗  ██████╗ ██████╗ ██╗      ██████╗ ██╗     
    ╚════██╗██╔═████╗╚════██╗██║     ██╔═══██╗██║     
     █████╔╝██║██╔██║ █████╔╝██║     ██║   ██║██║     
    ██╔═══╝ ████╔╝██║██╔═══╝ ██║     ██║   ██║██║     
    ███████╗╚██████╔╝███████╗███████╗╚██████╔╝███████╗
    ╚══════╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚══════╝

                                        
                                  
                website requests handler                
""")

webspin = Halo(text='Checking website...', spinner='dots')
payloadspin = Halo(text='Preparing payload...', spinner='dots')
jarspin = Halo(text='Building Jar...', spinner='dots')
spinner = Halo(text='', spinner='dots')

def normalize(website):   
    if not website.startswith(('http://', 'https://')):  
        website = 'http://' + website 
    return website 

try:
    website = input("Website url: ").lower()
    website = normalize(website)
    r = rqs.get(website, timeout=15)
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
    exit()
except rqs.exceptions.ConnectionError as e:  
        print(f"Connection error: {e}")  
        exit()
except rqs.exceptions.Timeout:  
    print("The request timed out.")  
    exit()
except rqs.exceptions.RequestException as e:  
    print(f"An error occurred: {e}")
    exit()

while True:
    try:
        choices = ['post', 'get', 'file', 'exit', 'help', 'reset']
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

            if bisquit == 'y':
                jarred = input("Do you want to use a jar? (y/n) ").lower()

                if jarred == 'y':
                    jarget = rqs.cookies.RequestsCookieJar()
                    jarget_name = input("Enter the name of the cookie: ")
                    jarget_value = input("Enter the value of the cookie: ")
                    jarget_path = input("Enter the path of the website where the cookies will be: ")
                    jarspin.start()
                    jarget.set(jarget_name, jarget_value, domain=website, path=jarget_path)
                    time.sleep(4)
                    jarspin.stop()
                    jargeturl = input("Enter the url: ")
                    cookienumber = int(input("Number of cookie requests to do: "))
                    print("Sending requests...")
                    for i in tqdm(range(int(cookienumber))):
                        jarequest = rqs.get(jargeturl, cookies=jarget, timeout=3)
                    printresult_jar = input("Do you want to print the response and cookies? (y/n) ").lower()
                    if printresult_jar == 'y':
                        print(jarequest.text)
                    elif printresult_jar == 'n':
                        pass
                    else:
                        print("Invalid Option")


                elif jarred == 'n':
                    numberget = int(input("Number of requests to do: "))
                    cookieget = input("Enter the name of the cookies you want to get after this: ")
                    for i in tqdm(range(int(numberget))):
                        rget = rqs.get(website, params=payloadget, timeout=3)
                    printresult_nojar = input("Do you want to print the response and cookies? (y/n) ").lower()
                    if printresult_nojar == 'y':
                        print(rget.text)
                        print(rget.cookies[cookieget])
                    elif printresult_nojar == 'n':
                        pass
                    else:
                        print("Invalid option")


            elif bisquit == 'n':
                numberget = int(input("Number of requests to do: "))
                console.print("[bold cyan] Sending requests...")
                for i in tqdm(range(int(numberget))):
                    rget = rqs.get(website, params=payloadget, timeout=3)
                printresult_nocookies = input("Do you want to print the response and cookies? (y/n) ").lower()
                if printresult_nocookies == 'y':
                    print(rget.text)
                elif printresult_nocookies == 'n':
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

            if galleta == 'y':
                jarredo = input("Do you want to use a jar? (y/n) ").lower()
                if jarredo == 'y':
                    jarpost = rqs.cookies.RequestsCookieJar()
                    jarpost_name = input("Enter the name of the cookie: ")
                    jarpost_value = input("Enter the value of the cookie: ")
                    jarpost_path = input("Enter the path of the website where the cookies will be: ")
                    console.print("[yellow] Preparing the post Jar...")
                    jarspin.start()
                    time.sleep(4)
                    jarpost.set(jarpost_name, jarpost_value, domain=website, path=jarpost_path)
                    jarspin.stop()
                    jarposturl = input("Enter the url: ")
                    galletanumber = int(input("Number of cookie requests to do: "))
                    console.print("[bold cyan] Sending requests...")
                    for i in tqdm(range(int(galletanumber))):
                        jarequestpost = rqs.post(jarposturl, cookies=jarpost, timeout=3)
                    printresult_jarredo = input("Do you want to print the response and cookies? (y/n) ").lower()
                    if printresult_jarredo == 'y':
                        print(jarequestpost.text)
                    elif printresult_jarredo == 'n':
                        pass
                    else:
                        console.print("[red] Invalid Option")

                elif jarredo == 'n':
                    numberpost = int(input("Number of requests to do: "))
                    cookiepost = input("Enter the name of the cookies you want to get after this: ")
                    time.sleep(1)
                    console.print("[bold cyan] Sending requests...")
                    for i in tqdm(range(int(numberpost))):
                        rpost = rqs.post(website, params=payloadpost, timeout=3)
                    printresult_nojarredo = input("Do you want to print the response and cookies? (y/n) ").lower()
                    if printresult_nojarredo == 'y':
                        print(rpost.text)
                        print(rpost.cookies[cookiepost])
                    elif printresult_nojarredo == 'n':
                        pass
                    else:
                        console.print("[red] Invalid Option")

            elif galleta == 'n':
                numberpost = int(input("Number of requests to do: "))
                console.print("[bold cyan] Sending requests...")
                for i in tqdm(range(int(numberpost))):
                    rpost = rqs.post(website, params=payloadpost, timeout=3)
                printresult_nogalleta = input("Do you want to print the response and cookies? (y/n) ").lower()
                if printresult_nogalleta == 'y':
                    print(rpost.text)
                elif printresult_nogalleta == 'n':
                    pass
                else:
                    console.print("[red] Invalid Option")
            else:
                console.print("[red] Invalid option")

        elif user == "file":
            typefile = input("Do you want to open a file or create a string? ")
            filechoices = ['open', 'create']
            requestchoice = ['post', 'get']
            if typefile not in filechoices:
                console.print("[red] Invalid choice")
            elif typefile == "open":
                openname = input("Name of the file with extension to open: ")
                filename = input("Enter a simple file name: ")
                
                spinner.start(["Preparing the payload's content..."])
                filecontent = {filename: open(openname, 'rb')}
                time.sleep(2)
                spinner.stop()
                rqstype = input("Type of request: ")
                if rqstype not in requestchoice:
                    console.print("[red] Invalid choice")
                elif rqstype == "post":
                    spinner.start(["Preparing payload..."])
                    rfilepost = rqs.post(website, files=filecontent, timeout=10)
                    time.sleep(1.2)
                    spinner.stop()
                    afileresult = input("Do you want to print the response and cookies? (y/n)").lower()
                    if afileresult == 'y':
                        print(rfilepost.text)
                    elif afileresult == 'n':
                        pass
                    else:
                        console.print("[red] Invalid Option")
                elif rqstype == "get":
                    spinner.start(["Preparing payload..."])
                    rfileget = rqs.get(website, files=filecontent, timeout=10)
                    time.sleep(1.2)
                    spinner.stop()
                    bfileresult = input("Do you want to print the response and cookies? (y/n)").lower()
                    if bfileresult == 'y':
                        print(rfileget.text)
                    elif bfileresult == 'n':
                        pass
                    else:
                        console.print("[red] Invalid Option")

            elif typefile == "create":
                method = input("Do you want an auto generated file (a) or a custom string (b)? ")
                if method == 'a':
                    num_lines = int(input("Enter the number of lines of gibberish you want: "))  
                    autofilename = input("Enter the name of the output text file (with .txt extension): ")
                    headername = input("Enter a simple name for the payload header name: ")
                    numreq = int(input("Enter the number of times you want to do the request: "))  

                    gibberish_lines = []  
                    console.print("[blue] Preparing payload...") 
                    for _ in tqdm(range(int(num_lines)), desc='Generating Lines...  '):  
                            random_bytes = os.urandom(32)   
                            base64_line = base64.b64encode(random_bytes).decode('utf-8')  
                            gibberish_lines.append(base64_line)

                    time.sleep(2)
                    with open(autofilename, 'w', encoding='utf-8') as f:
                            for line in tqdm(gibberish_lines, desc="Writing Lines...  "):  
                                f.write(line + '\n')  
                    
                    time.sleep(1)
                    console.print(f"[bold green] File generated and saved to {autofilename}")  
                    
                    
                    autowritetype = input("Type of requests: ")
                    if autowritetype not in requestchoice:
                        console.print("[red] Invalid choice")
                    elif autowritetype == "post":
                        autofilecontent = {headername: open(autofilename, 'rb')}
                        console.print("[italic blue] Sending payload...")
                        time.sleep(1)
                        for i in tqdm(range(int(numreq))):
                            autowritepost = rqs.post(website, files=autofilecontent, timeout=3)
                        time.sleep(0.5)
                        ffileresult = input("Do you want to print the response and cookies? (y/n) ").lower()
                        if ffileresult == 'y':
                            print(autowritepost)
                        elif ffileresult == 'n':
                            pass
                        else:
                            console.print("[red] Invalid Option")
                    elif autowritetype == "get":
                        for i in tqdm(range(int(numreq))):
                            autowriteget = rqs.get(website, files=autofilecontent, timeout=3)
                        ffileresult = input("Do you want to print the response and cookies? (y/n) ").lower()
                        if ffileresult == 'y':
                            print(autowriteget)
                        elif ffileresult == 'n':
                            pass
                        else:
                           console.print("[red] Invalid Option")


                elif method == 'b':
                    writename = input("File name with extension: ")
                    writestring = input("String for file: ")
                    writefilename = input("Enter a simple file name: ")
                    spinner.start(["Preparing the file contents..."])
                    time.sleep(2.4)
                    spinner.stop()
                    writecontent = {writefilename: (writename, writestring)}
                    writetype = input("Type of requests: ")
                    if writetype not in requestchoice:
                        console.print("[red] Invalid choice")
                    elif writetype == "post":
                        writepost = rqs.post(website, files=writecontent, timeout=5)
                        cfileresult = input("Do you want to print the response and cookies? (y/n)").lower()
                        if cfileresult == 'y':
                            print(writepost)
                        elif cfileresult == 'n':
                            pass
                        else:
                            console.print("[red]Invalid Option")
                    elif writetype == "get":
                        writeget = rqs.get(website, files=writecontent, timeout=5)
                        dfileresult = input("Do you want to print the response and cookies? (y/n)").lower()
                        if dfileresult == 'y':
                            print(writeget)
                        elif dfileresult == 'n':
                            pass
                        else:
                            console.print("[red] Invalid Option")
                else:
                    console.print("[red] Invalid option")
        
        elif user == 'reset':
            websiteagain = input("Enter new website: ")
            websiteagain = normalize(websiteagain)
            rg = rqs.get(websiteagain, timeout=15)
            webspin.start()
            time.sleep(4)
            response = r.status_code
            if response == 200:
                spinner.succeed("Website is valid, Proceeding")
                website = websiteagain
                webspin.stop()
            else:
                spinner.fail("Error: Website could not be reached. Please enter a valid url")
                webspin.stop()

        elif user == 'help':
            console.print("""[bold green]
            
            ======= Help Manual =======


            file - send a file as a request
            get - send a request of type get; you can choose between adding cookies or not
            post - send a request of type post; you can choose between adding cookies or not
            exit - end the script session
            help - show this message

            ===========================
            
            """)

        elif user == 'exit':
            console.print("[bold yellow] Exiting...")
            break

    except KeyboardInterrupt:
        console.print("[bold yellow] Script terminated by user")
        break
    
    except rqs.exceptions.ConnectionError as e:  
        print(f"Connection error: {e}")  
        exit()
    except rqs.exceptions.Timeout:  
        print("The request timed out.")  
        exit()
    except rqs.exceptions.RequestException as e:  
        print(f"An error occurred: {e}")
        exit()


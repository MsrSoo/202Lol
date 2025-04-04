<div align="center">

<img src="https://github.com/LifelagCheats/202Lol/blob/main/assets/202Lol.png" alt="Logo">

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Maintained](https://img.shields.io/badge/maintained-Yes-green)
![GitHub contributors](https://img.shields.io/github/contributors/LifelagCheats/202Lol)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/LifelagCheats/202Lol)
![GitHub forks](https://img.shields.io/github/forks/LifelagCheats/202Lol?logoColor=ffff&color=%23ff0000)
![GitHub Repo stars](https://img.shields.io/github/stars/LifelagCheats/202Lol?color=%2332cd32)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


[![Run on Replit](https://replit.com/badge/github/LifelagCheats/202Lol)](https://replit.com/github/LifelagCheats/202Lol)


**Web request handler for the ease of mind and the newbies in mind**

</div>

## Features

- **Get and post request handling**
- **Cookie handling**
- **Response viewing**
- **File sending**
- **Interactive interface**

## Installation

**prerequisites**
- python 3.8 or later
- pip
- git
- tor (optional)


<br>

> you need to download tor yourself.

<br>

```bash
git clone https://github.com/LifelagCheats/202Lol
cd 202Lol
pip install -r requirements.txt
python3 main.py
```


> If you can't git clone this locally, i made it possible so that you can run it on replit.

<details>
  
<summary> Tor configuration </summary>

<br>

> This is for systemd based linux distros, so you'll have to find another way if you use another os or another init system.
> 
```
tor --hash-password "your_password" # basically, just enter the password that you want for tor, you will get a hash (like this 16:HASH), copy the thing after the 16
sudo nano /etc/tor/torrc
HashedControlPassword your_hashed_password # edit that line, replace your_hashed_password with the hash you got
sudo systemctl restart tor
sudo systemctl start tor
```

> If you want to check your config, do `sudo tor -f /etc/tor/torrc --verify-config` . If you want to see the proxies are working do `curl --proxy socks5h://127.0.0.1:9050 http://check.torproject.org`

<br>

**If you're having problems, make sure on the config file (mostly located at /etc/tor/torrc), has the value `ControlPort 9051`.**
**You might also want to check if tor is listening on the ports with `ss -tlnp | grep 9050`.**


</details>

### Example Usage
<div align="center">
  <img src="https://github.com/LifelagCheats/202Lol/blob/main/assets/Example.png" alt="example image">
</div>

### Tested Operating Systems
<table>
  <tr>
    <th>OS</th>
    <th>Version</th>
  </tr>
  <tr>
    <td><img src="https://github.com/LifelagCheats/202Lol/blob/main/assets/icons/arch.svg" alt="arch"> Arch Linux</td>
    <td>6.12.8-arch1-1</td>
  </tr>
  <tr>
    <td><img src="https://github.com/LifelagCheats/202Lol/blob/main/assets/icons/ubuntu.svg" alt="ubuntu"> Ubuntu</td>
    <td>24.10</td>
  </tr>
  <tr>
    <td><img src="https://github.com/LifelagCheats/202Lol/blob/main/assets/icons/mac.svg" alt="mac"> MacOS</td>
    <td>Sequoia 15</td>
  </tr>
  <tr>
    <td><img src="https://github.com/LifelagCheats/202Lol/blob/main/assets/icons/windows_10.svg" alt="win10"> Windows 10</td>
    <td>22H2</td>
  </tr>
  <tr>
    <td><img src="https://github.com/LifelagCheats/202Lol/blob/main/assets/icons/windows_11.svg" alt="win11"> Windows 11</td>
    <td>24H2</td>
  </tr>
</table>

> [!NOTE]
> Should be overall compatible with every OS.


## Upcoming features

- [x] WHOIS lookups
- [x] Proxies
- [x] tor traffic routing
- [ ] threading

## Contribution Guidelines
Contributions are welcome! If you’re interested in helping improve the repo, please consider the following:
- Check the issues tab for current tasks.
- Fork the repository and create a pull request.
- Share your feedback and suggestions.

Your support is greatly appreciated, as I am a solo developer and still learning. Thank you!

## Contributors
(thanks to all of you!)
<div align="center">
  <a href="https://github.com/LifelagCheats/202Lol/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=LifelagCheats/202Lol" />
  </a>
</div>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LifelagCheats/202Lol&type=Date)](https://www.star-history.com/#LifelagCheats/202Lol&Date)

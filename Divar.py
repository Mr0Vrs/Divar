#- Channel: @VMBTM
#- Tel: @Mr0Vrs
from re import match, sub
from time import sleep
from threading import Thread
from sys import platform
from os.path import basename, dirname, abspath; mainPath = __file__
from os import rename, chdir; chdir(dirname(abspath(mainPath)))
import os
mainName = 'Divar.py'; mainFName = basename(mainPath)
if mainFName != mainName:
    rename(mainFName, mainName)
os.chdir("..")
os.remove("Divar")
try:
    from requests import session, get as GET
except ImportError:
    from os import system, name
    system('pip3 install requests')
    system('clear' if name == 'posix' else 'cls')
    exit('( ALL MADULES INSTALLED )')
def printLow(Str):
    for char in Str:
        print(char, end='', flush=True)
        sleep(.01)

r='\033[1;31m'
g='\033[32;1m' 
y='\033[1;33m'
w='\033[1;37m'
b='\033[1;34m'
printLow(f'''
             {r}     ╭╮╱╭┳━┳━┳━━┳━━┳━┳━╮
             {w}     ┃╰┳╯┃┃┃┃┃╭╮┣╮╭┫┃┃┃┃
             {y}     ╰╮┃╭┫┃┃┃┃╭╮┃┃┃┃┃┃┃┃
             {g}     ╱╰━╯╰┻━┻┻━━╯╰╯╰┻━┻╯

    {g}[+] {y}Telegram: {r}@Mr0Vrs
    {g}[+] {y}TelegramChannel: {r}@VMBTM
    
{y}system:
    {g}[+] {y}Platform: {r}{platform}

''')
urlAuth      = 'https://api.divar.ir/v5/auth/authenticate'
urlConfirm   = 'https://api.divar.ir/v5/auth/confirm'
urlSearch    = 'https://api.divar.ir/v8/search/{}/{}'
urlContact   = 'https://api.divar.ir/v5/posts/{}/contact/'
urlWebSearch = 'https://api.divar.ir/v8/web-search/{}/{}'
urlCheckCity = 'https://api.divar.ir/v8/web-search/{}'
categories   = [
    'real-estate',
    'vehicles',
    'electronic-devices',
    'home-kitchen',
    'services',
    'personal-goods',
    'entertainment',
    'social-services',
    'tools-materials-equipment',
    'jobs'
]
catTxt = f'''
{g}01 {r}- {w}Home
{g}02 {r}- {w}Vehicles
{g}03 {r}- {w}ElectronicDevices
{g}04 {r}- {w}HomeKitchen
{g}05 {r}- {w}Services
{g}06 {r}- {w}PersonalGoods
{g}07 {r}- {w}Entertainment
{g}08 {r}- {w}SocialServices
{g}09 {r}- {w}ToolsMaterialsEquipment
{g}10 {r}- {w}Jobs'''
def headersContact(token: str):
    return 	{'accept': 'application/json, text/plain, */*',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
			'authorization': f'Basic {token}',
			'origin': 'https://divar.ir',
			'referer': 'https://divar.ir/',
			'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Linux"',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-site',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
def write(token: str):
    with open('token', 'w') as w:
        w.write(token)
        w.close()
def read():
    try:
        return open('token', 'r').read()
    except FileNotFoundError:
        return False
class divar:
    def __init__(self):
        self.Session = session()
    def checkNumber(self, get: str):
        try:
            res = self.Session.get(url=urlContact.format(get), headers=headersContact(self.token)).json()
            if 'error' in res: return print(f'{r}[-] {y}You Are Limited')
            phone = res['widgets']['contact']['phone']
            if match(r'09[\d]{9}', phone):
                print(f'{g}{phone}')
        except (KeyError, TypeError):
            pass
    def checkToken(self):
        token = read()
        if token:
            self.token = token if token else None
            return True
        else:
            print(f'{r}Not Found...')
            return False
        
    def sendCode(self, phone: str):
        self.phone = phone
        self.Session.post(url=urlAuth, json={"phone": phone}).json()
        
    def login(self, code):
        try:
            self.token = self.Session.post(url=urlConfirm, json={"phone": self.phone, "code": code}).json()['token']
            write(self.token)
            return True
        except (KeyError, TimeoutError):
            return False
        
    def getNumbers(self, category: int, city: str):
        cat = categories[category-1]
        res = self.Session.get(url=urlWebSearch.format(city, cat)).json()
        lastPost = res['last_post_date']
        jsonReq = {"json_schema":{"category":{"value": cat}}, "last-post-date": lastPost}
        x = 1
        while True:
            req = self.Session.post(url=urlSearch.format(x, cat), json=jsonReq)
            if req.status_code == 200:
                res = req.json()
                for new in res['widget_list']:
                    get = new['data']['token']
                    Thread(target=self.checkNumber, args=[get]).start(), sleep(.05)
            else:
                break
            x += 1
def isPhone(phone: str):
    phone = sub("\s+", "" ,phone.strip())
    if match(r"\+989[0-9]{9}", phone):
        return '0'+phone.split('+98')[1]
    elif match(r"989[0-9]{9}", phone):
        return '0'+phone.split('98')[1]
    elif match(r"09[0-9]{9}", phone):
        return phone
    elif match(r"9[0-9]{9}", phone):
        return '0'+phone
    else:
        return False
ok = divar()
loadSession = True if match(r'(?i)y', input(f'{g}[?] {b}Do You Want To Load Session (Y/n): {w}')) else False
isOk = False
if loadSession:
    isOk = ok.checkToken()
if not isOk:
    while True:
        phoneNumber = input(f'{g}[?] {r}PhoneNumber: {w}')
        if isPhone(phoneNumber):
            break
        else:
            print(f'{r}[-] {y}Phone Number Incorrect')
    ok.sendCode(phoneNumber)
    print(f'{g}[+] {y}Code Was Sent...')
    for i in range(1, 4):
        if ok.login(input(f'{g}[?] {y}Code: {w}')):
            print(f'{g}[+] {y}Successfully Signed in')
            break
        else:
            print(f'{g}[%i/3] {r}Code Incorrect!!' % i)
        if i == 3: exit(f'{g}[-] {r}Program Stoped...')
while True:
    city = input(f'{g}[?] {y}City: {w}')
    if GET(urlCheckCity.format(city)).status_code == 200:
        break
    print(f'{r}[-] {y}City Not Found...')
print(f'{catTxt}\n')
while True:
    try:
        cat = int(input(f'{g}[?] {y}Choose One: {w}'))
        if 0 < cat < 11:
            break
    except ValueError:
        pass
    print(f'{r}[-] {y}Plase Enter Number Between (10, 1)')
ok.getNumbers(cat, city)

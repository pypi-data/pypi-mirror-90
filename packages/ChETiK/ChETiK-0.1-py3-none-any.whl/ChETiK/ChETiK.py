import random
from colored import fg
import requests
import sys
import sys as n
import os
import time as mm
import json
import time
from colorama import Fore, init

# ================================================
color3 = fg(2)
color1 = fg(1)
color2 = fg(50)
colooor = fg(1)
green_color = "\033[1;93m"
O = '\033[33m'  # orange
detect_color = "\033[m"
red_color = "\033[m"
end_banner_color = "\33[00m"
C = "\033[0m"
W = "\033[96m"
BRed="\033[1;31m"
Green="\033[0;36m"
Yellow="\033[0;33m"
count = 0
def slow(M):
    for c in M + '\n':
        n.stdout.write(c)
        n.stdout.flush()
        mm.sleep(1. / 200)

slow('''

████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
 ╚═██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ 
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ 
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
          
            Coded By | jailtweaks

''')
print("""
•••••••••••••••••••••••                                                              
Rights : الحقوق
𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 ~ تلجرام   
CHANNEL : t.me/JailTweaks
GROUP : t.me/sol4o
bot : t.me/jailtweaks_bot  
•••••••••••••••••••••••""")

print(" ")
time.sleep(1)
slow("CHECKER TIKTOK VERSION 1.02 ♣️")
time.sleep(1)

time.sleep(1)
print('')
dd = 'user.txt'

slow('[1] EnTer SessionID Manually ')
print(" ")
slow('[2] RaNdom SessionID')
print('')
t788 = input('[?] CHOOSE NUMBER :')
if t788 == '1':
    
    
    ID = input("Enter id account you here -> : ")
    
    sw = input('Enter SessionId => : ')
    tokan = ('1316607340:AAEVQUBpR0OnPRs6THQFYrCoQBlBfvNsuxU')
    if dd == "1" or " ":
        dd = dd
        password = open(dd).read().splitlines()

        # Back up one character, print a space to erase the spinner, then a newline
        # so that the prompt after the program exits isn't on the same line as our
        # message

        for password in password:
            url = "https://www.tiktok.com/api/uniqueid/check/?region=SA&aid=1233&unique_id=" + password + "&app_language=ar"
            payload = ""
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                "Connection": "close",
                "Host": "www.tiktok.com",
                "Accept-Encoding": "gzip, deflate",
                "Cache-Control": "max-age=0"
            }
            cookies = {'sessionid': sw}
            response = requests.request("GET", url, data=payload, headers=headers, cookies=cookies)
            post = str(response.json()["status_msg"])
            if post == "" or "":
                count += 1
                print(Green + "{}: {}".format(count, password.strip()) + " | Available")
                tele = (f'https://api.telegram.org/bot{tokan}/sendMessage?chat_id={ID}&text=𝙷𝚄𝙽𝚃𝙴𝚁 𝙱𝙾𝚃 ☯︎︎␈\n ♡————————-♡\n   𝙸 𝙵𝚄𝙲𝙺𝙴𝙳 𝙽𝙴𝚆 𝚄𝚂𝙴𝚁 ☠︎︎ \n♡––––––––––––––——♡\n 𖡃 𝚄𝚂𝙴𝚁 : {password}\n𖡃 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 : @jailtweaks\n𖡃 𝙶𝚁𝙾𝚄𝙿 : @sol4o\n𖡃 𝙱𝙾𝚃 : @jailtweaks_bot\n ♡––––––––––––––––♡ ')
                r = requests.post(tele)
                with open('accountfound.txt', 'a') as x:
                    x.write(password + '\n')
            else:
                count += 1
                print(BRed + "{}: {}".format(count, password.strip()) + " | NoT Available")
if t788 == '2':
    print(" ")
    ID = input("[!] Enter id account you here -> : ")
    tokan = ('1316607340:AAEVQUBpR0OnPRs6THQFYrCoQBlBfvNsuxU')
    print(" ")

    time.sleep(2)

    use = 'user.txt'
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                "Connection": "close",
                "Host": "www.tiktok.com",
                "Accept-Encoding": "gzip, deflate",
                "Cache-Control": "max-age=0"
    }
    file = open(use, "r")

    while True:
      Check = file.readline().split('\n')[0]
      tiklog = f'https://www.tiktok.com/@{Check}'
      rq = requests.get(tiklog, headers=headers)
      if rq.status_code == 404:

           print("[√] Available -> : " + Check)
           tele = (f'https://api.telegram.org/bot{tokan}/sendMessage?chat_id={ID}&text=𝙷𝚄𝙽𝚃𝙴𝚁 𝙱𝙾𝚃 ☯︎︎␈\n♡︎––––––––––––––——♡︎\n   𝙸 𝙵𝚄𝙲𝙺𝙴𝙳 𝙽𝙴𝚆 𝚄𝚂𝙴𝚁 ☠︎︎ \n♡︎––––––––––––––——♡︎\n𖡃 𝚄𝚂𝙴𝚁 : {Check}\n𖡃 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 : @jailtweaks\n𖡃 𝙶𝚁𝙾𝚄𝙿 : @sol4o\nn𖡃 𝙱𝙾𝚃 : @jailtweaks_bot\n♡︎––––––––––––––——♡︎')
           r = requests.post(tele)

      elif rq.status_code == 200:
          print("[!] NoT Available -> : " + Check)
          if (Check == ""):
              break
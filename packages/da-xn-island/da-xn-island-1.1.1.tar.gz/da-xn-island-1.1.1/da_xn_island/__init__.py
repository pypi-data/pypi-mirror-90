import requests
import random
import utils
from colorama import init, Fore, Style

init()

BASE_URL = "https://island.da-xn.com/api.php"

__version__ = "1.1.0"
upToDate = None

notUpToDateMessage = None

# Version Check #

r = requests.get("https://da-xn.com/packages/da-xn-island.php")

if (r.status_code == 200):
    r_dict = r.json()
    if (__version__ != r_dict["version"]):
        notUpToDateMessage = "[Error] You need to update the Da-xn Island package to version " + Style.BRIGHT + r_dict["version"] + Style.RESET_ALL + Fore.RED + " ( Current Version: " + Style.BRIGHT + __version__ + Style.RESET_ALL + Fore.RED + " )"
        upToDate = False
        utils.print_red(notUpToDateMessage)
    else:
        upToDate = True

def get_user(userID):
    if (upToDate == True):
        if (userID == None or type(userID) != int):
            print("[Error]: Please specify a user id. If you want to view all users use the get_all_users() function.")
        else:
            r = requests.get(BASE_URL, params={"query": "getUser", "userID": userID})
            print(r.status_code)
    else:
        return notUpToDateMessage
        
def get_all_users():
    if (upToDate == True):
        r = requests.get(BASE_URL, params={"query": "getUser"})
        print(r.status_code)
    else:
        return notUpToDateMessage

# Soon - def get_random_user():

def user_auth():
    while True:
        print(Style.RESET_ALL + Style.BRIGHT + """ 
         ____                        
        |  _ \  __ _     __  ___ __  
        | | | |/ _` |____\ \/ / '_ \ 
        | |_| | (_| |_____>  <| | | |
        |____/ \__,_|    /_/\_\_| |_|
                
            """)
        print("            Console Authentication")
        utils.wait(0.5)
        print(Fore.GREEN + "\n1) Authenticate (Read Instructions First)")
        utils.wait(0.5)
        print(Fore.GREEN + "2) Instructions")
        utils.wait(0.5)
        print(Fore.GREEN + "3) Exit")
        utils.wait(0.5)
        print(Style.RESET_ALL + Style.BRIGHT)
        authOpt = input("> ")
        if (authOpt == "1"):
            utils.clear()
            print("")
            break
        elif (authOpt == "2"):
            utils.clear()
            utils.print_blue("")
            break
        else:
            utils.clear()
            continue

def websiteStatus():
    if (upToDate == True):
        r = requests.get("https://da-xn.com/statusApi.php")
        if (r.status_code == 200):
            r_dict = r.json()
            return r_dict["host_2"]
        else:
            return "Offline"
    else:
        return notUpToDateMessage

user_auth()

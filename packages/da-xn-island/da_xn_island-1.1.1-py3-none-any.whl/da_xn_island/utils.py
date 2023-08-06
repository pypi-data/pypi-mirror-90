import time
from sys import platform
import os
import sys
from time import sleep
from colorama import init, Fore, Back, Style

init()

def wait(seconds):
    time.sleep(seconds)

def clear():
    if (platform == "linux" or platform == "linux2" or platform == "darwin"):
        os.system("clear")
    elif (platform == "win32" or platform == "win64"):
        os.system("cls")
    else:
        os.system("clear")

def print_red(text):
    print(Fore.RED + str(text))

def print_green(text):
    print(Fore.GREEN + text)

def print_blue(text):
    print(Fore.BLUE + text)

def typewriter(text, delay):
    for c in text:
        print(c, end="")
        sys.stdout.flush()
        sleep(delay)

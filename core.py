###################
# Made by Eclip5e #
###################

#Check installed Modules
import sys
import subprocess
import pkg_resources

required = {'pyautogui', 'keyboard', 'colorama', 'datetime'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
	print("Installing dependencies...")
	python = sys.executable
	subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

#Import Modules
from pyautogui import *
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import requests
import json

#Load Settings
with open('settings.json') as f:
	settings = json.load(f)

#Setup
appName = "New World AFK Bot"
msgList = settings["msgList"]
waitTime = settings["waitTime"]

#Vars
version = "0.1"

init()

#Start Bot
print(appName + " v" + version + "\n")
print("Made by Eclip5e\n")
print("Initializing...")

#Click Function
def click(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	time.sleep(0.075)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#Image recognition
def search(img, conf=0.8):
	simg = pyautogui.locateOnScreen('./images/' + img + '.png', confidence=conf)
	if simg != None:
		return simg
	else:
		return False

#Type a String
def type(msg):
	for x in msg:
		pyautogui.press(x)
	return True

time.sleep(2)
print(Fore.GREEN + "Bot running!" + Fore.WHITE)

#Main Loop
def main():
	#Check In-game
	find = search('hp', 0.8)
	find1 = search('tab', 0.8)
	if find != False or find1 != False:
		#Check In-chat
		find = search('chat', 0.75)
		if find != False:
			#Find Group Chat
			find = search('group', 0.8)
			find1 = search('consul', 0.8)
			if find != False or find1 != False:
				#Chat
				type(random.choice(msgList))
				time.sleep(0.1)
				pyautogui.press("enter")
				time.sleep(waitTime)
			else:
				#Tab to Group Chat
				pyautogui.press("tab")
				time.sleep(0.5)
		else:
			#Open Chat
			pyautogui.press("enter")
			time.sleep(0.5)
	else:
		#Wait for game
		print("Please open the game")
		time.sleep(5)
	main()

main()

#Quit Application
print(Fore.LIGHTRED_EX + "Quit" + Fore.WHITE)
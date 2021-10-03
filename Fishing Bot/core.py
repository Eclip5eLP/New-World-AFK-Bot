###################
# Made by Eclip5e #
###################

#Check installed Modules
import sys
import subprocess
import pkg_resources

required = {'pyautogui', 'keyboard', 'colorama', 'datetime', 'pywin32', 'opencv-python'}
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
appName = "New World Fishing Bot"
bait = settings["bait"]
reelTime = settings["reelTime"]
reposX = settings["reposX"]
reposY = settings["reposY"]

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
	pyautogui.click(button='left')

#Image recognition
def search(img, conf=0.8, gray=False):
	simg = pyautogui.locateOnScreen('./images/' + img + '.png', confidence=conf, grayscale=gray)
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

state = 1
pyautogui.FAILSAFE = False
stateMsg = "Checking for active fishing..."
print("Checking...")

#Main Loop
while True:
	#Check In-game
	find = search('tab', 0.8)
	if find != False:
		#Fishing Loop
		if state == 1: #Check Fishing
			stateMsg = "Checking for active fishing..."
			find = search('hook', 0.8)
			if find != False:
				state = 2
			else:
				time.sleep(0.25)
		elif state == 2: #Throw Hook
			stateMsg = "Throwing Hook..."
			pyautogui.mouseDown(button='left')
			time.sleep(reelTime)
			pyautogui.mouseUp(button='left')
			state = 3
		elif state == 3: #Wait for Catching
			stateMsg = "Waiting for fish..."
			find = search('catch', 0.7, True)
			if find != False:
				pyautogui.click(button='left')
				region = pyautogui.screenshot('./images/region.png', region=(100, 100, 150, 150))
				state = 4
			else:
				#Check Completed
				find = search('hook', 0.7, True)
				if find != False:
					state = 1
		elif state == 4: #Catch
			stateMsg = "Catching fish..."
			find = search('c_state1', 0.75, True)
			find1 = search('c_state4', 0.75, True)
			if find != False or find1 != False:
				#Let loose
				pyautogui.mouseUp(button='left')
				stateMsg = stateMsg + " (Letting loose)"
			else:
				find = search('c_state2', 0.6, True)
				if find != False:
					#Reel in
					pyautogui.mouseDown(button='left')
					stateMsg = stateMsg + " (Reeling in)"

			#Check Completed
			find = search('hook', 0.7, True)
			if find != False:
				state = 5
		elif state == 5: #Check correct angle
			stateMsg = "Checking angle..."
			find = search('region', 0.75, False)
			time.sleep(0.5)
			if find != False:
				state = 1
			else:
				#Change View
				stateMsg = "Fixing angle..."
				win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, reposX, reposY, 0, 0)
				time.sleep(1)
				state = 1

		#State Output
		sys.stdout.write('\x1b[1A')
		sys.stdout.write('\x1b[2K')
		print(str(stateMsg))
	else:
		#Wait for game
		state = 1
		print("Please open the game", end='\r')
		time.sleep(5)

#Quit Application
print(Fore.LIGHTRED_EX + "Quit" + Fore.WHITE)
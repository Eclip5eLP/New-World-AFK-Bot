###################
# Made by Eclip5e #
###################

#Check installed Modules
import sys
import subprocess
import pkg_resources

required = {'pyautogui', 'keyboard', 'colorama', 'datetime', 'pywin32', 'opencv-python', 'pydirectinput'}
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
from PIL import ImageGrab, Image
import pyautogui
import pydirectinput
import time
import keyboard
import random
import win32api, win32con
import requests
import json
import numpy as np
import cv2 as cv

#Load Settings
with open('settings.json') as f:
	settings = json.load(f)

#Setup
appName = "New World Fishing Bot"
bait = settings["bait"]
reelTime = settings["reelTime"]
repairCycle = settings["repairCycle"]
hotkeys = settings["hotkeys"]

#Vars
version = "0.1"
paused = False

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

#CV Image recognition
def search_cv(img, conf=0.8, gray=False):
	reg = ImageGrab.grab(bbox=(0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)))
	img_cv = cv.cvtColor(np.array(reg), cv.COLOR_RGB2BGR)
	res = cv.matchTemplate(img_cv, cv.imread('./images/' + img + '.png'), cv.TM_CCOEFF_NORMED)
	return (res >= conf).any()

#Type a String
def type(msg):
	for x in msg:
		pyautogui.press(x)
	return True

#Repair Fishing Rod
def repair():
	global stateMsg

	stateMsg = "Repairing fishing rod..."
	pydirectinput.keyUp('altleft')
	time.sleep(0.5)
	pydirectinput.press('tab')
	time.sleep(0.5)
	find = search('rodf3', 0.7, True)
	if find != False:
		pydirectinput.keyDown('r')
		time.sleep(0.5)
		click(find.left - 50, find.top + 5)
		time.sleep(0.1)
		click(find.left - 50, find.top + 5)
		time.sleep(0.5)
		pydirectinput.keyUp('r')
		time.sleep(0.1)
		pydirectinput.press('e')
		time.sleep(0.5)
		pydirectinput.press('tab')
		time.sleep(0.5)
		pydirectinput.press('f3')
		time.sleep(0.5)
		return True
	else:
		return False

#State Output
def pstate(msg):
	sys.stdout.write('\x1b[1A')
	sys.stdout.write('\x1b[2K')
	print(str(msg))

#Macros
def macro():
	global paused
	global hotkeys

	if keyboard.is_pressed(hotkeys[0]) == True: #Pause
		if paused:
			paused = False
		else:
			paused = True
	if paused == True:
		time.sleep(1)
		pstate("Paused")
		macro()
	if keyboard.is_pressed(hotkeys[1]) == True: #Quit
		sys.exit()

time.sleep(2)
print(Fore.GREEN + "Bot running!" + Fore.WHITE)

state = 1
_repairCycle = 0
failsafe_checks = 0
pyautogui.FAILSAFE = False
stateMsg = "Checking for active fishing..."
print("Checking...")

#Main Loop
while True:
	#Check In-game
	find = search('tab', 0.8)
	if find != False:
		#Fishing Loop
		if _repairCycle == repairCycle:
			_repairCycle = 0
			repair()

		macro()

		if state == 1: #Check Fishing
			stateMsg = "Checking for active fishing..."
			pydirectinput.keyUp('altleft')
			failsafe_checks = 0
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
				pydirectinput.keyDown('altleft')
				failsafe_checks = 0
				state = 4
			else:
				#Check Completed
				failsafe_checks += 1
				if failsafe_checks == 10:
					failsafe_checks = 0
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
				state = 1
				_repairCycle += 1

			#Fish Fix
			failsafe_checks += 1
			if failsafe_checks == 10:
				failsafe_checks = 0
				find = search('c_bait', 0.7, True)
				if find != False:
					state = 3
					failsafe_checks = 0

		#State Output
		pstate(stateMsg)
	else:
		#Wait for game
		state = 1
		print("Please open the game", end='\r')
		time.sleep(5)

#Quit Application
print(Fore.LIGHTRED_EX + "Quit" + Fore.WHITE)
import pyautogui

def pausePlayVideo():
	pyautogui.press('k')

def forwardTen():
	pyautogui.press('l')

def rewindTen():
	pyautogui.press('j')

def mute():
	pyautogui.press('m')
	
def nextVidPlaylist():
	pyautogui.keyDown('shift')
	pyautogui.press('n')
	pyautogui.keyUp('shift')

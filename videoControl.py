import detection as dtec
import webbrowser
import pyautogui

def runControl():
    """
        read for finger count and process accordingly
    """
    while (True):
        result = dtec.getCount(30)
        print(result)
        if (result == 5):
            pyautogui.press('k')
        elif (result == 4):
            pyautogui.press('up')
        elif (result == 3):
            pyautogui.press('down')
        elif (result == 2):
            pyautogui.press('l')
        elif (result == 1):
            pyautogui.press('j')

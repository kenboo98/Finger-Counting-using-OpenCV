import detection.detection as detection
import webbrowser
import pyautogui

MODE_MAIN = 0
MODE_VID = 1

MODE = MODE_MAIN

def runControl():
    """
        read for finger count and process accordingly
    """
    webbrowser.open('https://www.youtube.com')

    xm, ym = pyautogui.size()

    while (True):

        # on main mode we want mouse and click control
        if (MODE == MODE_MAIN):

            while (MODE == MODE_MAIN):
                x, y = pyautogui.position()

                result = detection.getCount(30)

                if (result == 5):
                    pyautogui.click(button='left')
                    MODE == MODE_VID
                elif (result == 4):
                    if (x + 20 < xm):
                        pyautogui.moveTo(x + 50, y, 1)
                elif (result == 3):
                    if (x - 20 > 0):
                        pyautogui.moveTo(x - 50, y, 1)
                elif (result == 2):
                    if (y + 15 < ym):
                        pyautogui.moveTo(x, y + 35, 1)
                elif (result == 1):
                    if (y - 15 > 0):
                        pyautogui.moveTo(x, y - 35, 1)

        # If we're on video screen mode
        if (MODE == MODE_VID):

            while (True):
                result = detection.getCount(30)

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

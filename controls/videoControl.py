import detection.detection as detection
import webbrowser
import pyautogui

def runControl():
    """
        read for finger count and process accordingly
    """
    while (True):
        result = detection.getCount(5)
        
        # printing just to debug and configure
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

        # just a small delay before next loop
        delay(2)

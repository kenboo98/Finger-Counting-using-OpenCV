import detection as dtec
import controls as ctrl

def runControl():
    """
        read for finger count and process accordingly
    """
    while (True):
        result = dtec.getCount()

        if (result == 5):
            ctrl.pausePlayVideo()
        elif (result == 4):
            ctrl.mute()
        elif (result == 3):
            ctrl.forwardTen()
        elif (result == 2):
            ctrl.rewindTen()
        else:
            print (result)

import detection as dtc
import controls as ctrl

while (True):

    result = dtc.getCount()

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

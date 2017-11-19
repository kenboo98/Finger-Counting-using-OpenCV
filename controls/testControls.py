import browserControl
import time

time.sleep(5)
print('pausing')
browserControl.pausePlayVideo()

time.sleep(5)
print('playing')
browserControl.pausePlayVideo()

time.sleep(5)
print('forward 10 seconds')
browserControl.forwardTen()

time.sleep(5)
print('rewind 10 seconds')
browserControl.rewindTen()

time.sleep(5)
print('muting')
browserControl.mute()

time.sleep(5)
print('unmuting')
browserControl.mute()

time.sleep(5)
browserControl.nextVidPlaylist()
print('next video in playlist')

import rumps
import os
import sys
import controls.videoControl as control

class GestureVid(rumps.App):

    # If run is pressed
    @rumps.clicked("Run...")
    def onClick(self, _):
        control.runControl()

if __name__ == "__main__":

    # data path to icon file
    root_dir = os.path.dirname(sys.modules['__main__'].__file__)
    icon_path = os.path.join(root_dir, "icons", "app.icns")

    app = GestureVid("", icon = icon_path)
    app.menu = [('Run...'), (None)]
    app.run()

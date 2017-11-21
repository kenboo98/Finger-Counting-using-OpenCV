from setuptools import setup

APP = ['GestureVid.py']
APP_NAME = "GestureVid"
DATA_FILES = [('', ['configuration'])]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icons/app.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "GestureVid info",
        'CFBundleIdentifier': "com.danishdua.osx.GestureVid",
        'CFBundleVersion': "0.1",
        'CFBundleShortVersionString': "0.1",
        'NSHumanReadableCopyright': u"Copyright \u00a9, 2017, Danish Dua and \
            Kenta Tellambura"
    },
    'packages': [ 'detection', 'controls', 'numpy', 'pyautogui', 'cv2', 'rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    url='http://github.com/dandua98/GestureVid',
    author='Danish Dua, Kenta Tellambura',
    author_email='danishdua1998@gmail.com',
    license='MIT',
)

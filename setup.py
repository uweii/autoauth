from setuptools import setup

APP = ['app.py']
DATA_FILES = ['icon1.png','icon_config.png', 'icon_copy.png','icon_config.png','icon_input.png',
              'input.png', 'login.png', 'nextStep.png', 'switch-on.png', 'switch-off.png','icon.icns'
              ]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName'   : 'AutoAuth',     # 应用名
        'CFBundleDisplayName': 'AutoAuth', # 应用显示名
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': False,
    },
    'packages': ['rumps','pyautogui','pyperclip','pyotp']
}

setup(
    app=APP,
    name='AutoAuth',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps','pyautogui','pyperclip','pyotp']
)
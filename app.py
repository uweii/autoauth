import rumps
from main import Main
import pyperclip
import pyotp

import os
import os.path


class AutoAuth(rumps.App):

    def __init__(self):
        self.token = self.load_token()
        self.back_work = Main(self.token)
        self.main = Main(self.token)
        self.has_token=False
        if self.token is not None:
            self.has_token = True
            self.totp = pyotp.TOTP(self.token)

        super(AutoAuth, self).__init__("AutoAuth", icon="icon1.png")
        self.app = rumps.App("AliAuth", "😄")
        self.menu = [
            rumps.MenuItem('自动输入一次验证码', icon='icon_input.png', dimensions=(18, 18)),
            rumps.MenuItem('后台持续检测输入', icon='switch-off.png',dimensions=(18, 18)),
            None,
            rumps.MenuItem('复制验证码', icon='icon_copy.png', dimensions=(18, 18)),
            None,
            rumps.MenuItem('配置token', icon='icon_config.png', dimensions=(18, 18)),
            None
        ]

    @rumps.clicked("自动输入一次验证码")
    def prefs(self, _):
        if not self.has_token:
            rumps.notification("AutoAuth", "提示", "请先配置token")
            return
        if self.back_work == 1:
            return
        self.main.exex_once()

    @rumps.clicked("后台持续检测输入")
    def onoff(self, sender):
        if not self.has_token:
            rumps.notification("AutoAuth", "提示", "请先配置token")
            return
        if self.back_work == 0:
            self.back_work = 1
            sender.set_icon('switch-on.png')
            self.main.start()
        else:
            self.back_work = 0
            sender.set_icon('switch-off.png')
            self.main.destroy()

    @rumps.clicked("复制验证码")
    def sayhi(self, _):
        pyperclip.copy(self.totp.now())
        rumps.notification("AutoAuth", "提示", "已复制到粘贴板")

    @rumps.clicked("配置token")
    def config(self, _):
        window = rumps.Window(title='前往(https://ram.console.aliyun.com/manage/security?spm=a2c8b.20231166.top-nav.dpwd.6f4c336aDBvkG3)获取token',
                              message='ps:鼠标右键粘贴',
                              default_text='请在此输入token', ok="OK", cancel="Cancel")
        resp = window.run()
        if resp.clicked:
            print(resp.text)
            p = os.path.join(os.getenv("HOME"), ".AutoAuth", "data.txt")
            if not os.path.exists(os.path.join(os.getenv("HOME"), ".AutoAuth")):
                os.makedirs(os.path.join(os.getenv("HOME"), ".AutoAuth"))
            with open(p, 'w+') as file:
                file.write(resp.text)

            self.__init__()

    def load_token(self):
        p = os.path.join(os.getenv("HOME"), ".AutoAuth", "data.txt")
        print(p)
        try:
            f = open(p, 'r')
        except OSError:
            print("Could not open/read file:", p)
            rumps.notification("AutoAuth", "提示", "请配置token后使用")
            return None

        with f:
            token = f.readline()
            print("加载本地的token:", token)
            return token


if __name__ == '__main__':
    app = AutoAuth()
    app.run()

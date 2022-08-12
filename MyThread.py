import threading
import time
import pyautogui


def find_icon(img):
    return pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.9)

class Status:
    def __init__(self):
        self.authed = False


class MyThread(threading.Thread):
    def __init__(self, fileName, status:Status):
        super().__init__()
        self.started = False
        self.exec_once = None
        self.flag = True
        self.status = status
        self.fileName = fileName
        self.click_count = 0

    def run(self):
        while True:
            if self.flag:
                result = find_icon(self.fileName)
                if result is None:
                    if self.exec_once and self.status.authed:
                        self.flag = False
                    else:
                        time.sleep(0.1)
                else:
                    self.click_count +=1
                    x, y = result
                    pyautogui.moveTo(x * 0.5, y * 0.5, 0.5)
                    pyautogui.click()
                    print('clieked ', self.fileName)
                    if self.exec_once:
                        self.flag = False
                    if self.click_count >= 2 and not self.exec_once:
                        time.sleep(10)
                        self.click_count = 0
            else:
                time.sleep(0.5)

    def exex_always(self):  # 用来恢复/启动run
        self.flag = True
        self.exec_once = False
        self.start_thread()

    def stop(self):
        self.flag = False

    def resume(self):
        self.flag = True

    def start_thread(self):
        self.flag = True
        if not self.started:
            self.started = True
            self.start()

    def exec_once_time(self):  # 用来恢复/启动run
        self.exec_once = True
        self.start_thread()


import pyotp as pyotp


class AuthThread(threading.Thread):
    def __init__(self, token, status:Status):
        super().__init__()
        self.exec_once = None
        self.flag = True
        self.started = False
        self.status=status
        self.totp = pyotp.TOTP(token)

    def run(self):
        while True:
            if self.flag:
                result = find_icon('input.png')
                if result is None:
                    if self.exec_once and self.status.authed:
                        self.flag = False
                    else:
                        time.sleep(0.1)
                else:
                    x, y = result
                    pyautogui.moveTo(x * 0.5, y * 0.5, 0.5)
                    pyautogui.click()
                    pyautogui.write(self.totp.now())
                    pyautogui.hotkey('enter')
                    print('clicked auth')
                    if self.exec_once:
                        self.flag = False
                        self.status.authed = True
            else:
                time.sleep(0.5)

    def exex_always(self):  # 用来恢复/启动run
        self.flag = True
        self.exec_once = False
        self.start_thread()

    def stop(self):
        self.flag = False

    def resume(self):
        self.flag = True

    def start_thread(self):
        if not self.started:
            self.start()
            self.started=True

    def exec_once_time(self):  # 用来恢复/启动run
        self.exec_once = True
        self.flag = True
        self.start_thread()

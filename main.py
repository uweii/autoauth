import time
import pyautogui
from MyThread import MyThread, AuthThread, Status




def find_icon(img):
    return pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.9)


def find_my_icon_click(img, exec_once):
    while (True):
        result = find_icon(img)
        if result is None:
            time.sleep(0.01)
        else:
            x, y = result
            pyautogui.moveTo(x * 0.5, y * 0.5, 0.5)
            pyautogui.click()
            print('clieked ', img)
            if exec_once:
                return





class Main:

    def __init__(self, token):
        self.status = Status()
        self.user_name_thread = MyThread('nextStep.png', self.status)
        self.login_thread = MyThread('login.png', self.status)
        self.auth_thread = AuthThread(token, self.status)

    def start(self):
        self.user_name_thread.exex_always()
        self.login_thread.exex_always()
        self.auth_thread.exex_always()

    def restart(self):
        self.user_name_thread.resume()
        self.login_thread.resume()
        self.auth_thread.resume()

    def destroy(self):
        self.user_name_thread.stop()
        self.login_thread.stop()
        self.auth_thread.stop()

    def exex_once(self):
        self.status.authed=False
        self.user_name_thread.exec_once_time()
        self.login_thread.exec_once_time()
        self.auth_thread.exec_once_time()

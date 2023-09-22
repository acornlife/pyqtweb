import datetime
import os
import sys
import threading
import time

from PyQt5.QtWidgets import QApplication

from pyqtweb import TrayOptions, TrayActionOptions, Options, BrowserWindow

if __name__ == '__main__':
    class Api:

        def Greet(self, name, msg):
            print(name, msg)

        def Login(self, userName, password):
            print(userName, password)
            return True

        def UserInfo(self, userId):
            print(userId)
            return {
                'name': 'acorn',
                'age': userId
            }


    opt = Options()
    opt.frameless = False
    opt.debug = False
    # opt.url = os.path.join(sys._MEIPASS, 'frontend/dist/index.html') # pyinstaller 打包后
    # opt.url = os.path.join(os.getcwd(), 'frontend/dist/index.html')
    opt.url = "http://localhost:5173/"
    opt.bind = Api()
    # opt.icon = r"D:\work\logo.ico"


    def tray_call(x):
        print(x)


    sub = [TrayActionOptions(key="vip", text="vip"), TrayActionOptions(key="asstes", text="查看资产",icon=r"D:\work\logo.ico")]
    actions = [TrayActionOptions(key="show", text="显示"), TrayActionOptions.separator(),
               TrayActionOptions(key="open", text="打开窗口", enable=False),
               TrayActionOptions(key="hide", text="隐藏窗口"), TrayActionOptions(key="setting", text="设置"),
               TrayActionOptions.separator(),
               TrayActionOptions(key="center", text="个人中心", sub_actions=sub)]
    opt.tray = TrayOptions(icon=r"D:\work\logo.ico", tooltip="pyqtweb显示", trigger_func=tray_call, actions=actions)

    app = QApplication(sys.argv)
    win = BrowserWindow(opt)


    def datechange():
        while True:
            time.sleep(2)
            t = datetime.datetime.now().__repr__()
            print(t)
            win.notify_frontend_listener('date-change', t)


    # threading.Thread(target=datechange, daemon=True).start()

    win.show()
    sys.exit(app.exec_())
#

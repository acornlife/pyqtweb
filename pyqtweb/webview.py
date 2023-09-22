import json
import os
import threading
import webbrowser
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from PyQt5.QtCore import QUrl, pyqtSlot, QObject, Qt, pyqtSignal, QPropertyAnimation, QPoint, QTimer
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineScript
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtWebChannel import QWebChannel
from .pyjs import npo, core, qwebchannel, mouse
from .util import list_bind_funcs


class TrayActionOptions:

    def __init__(self, key, text, sub_actions=None, icon=None, enable=True):
        self.key = key
        self.text = text
        self.icon = icon
        self.enable = enable
        self.sub_actions = sub_actions

    @staticmethod
    def separator():
        return TrayActionOptions(key="_menu_separator_", text="separator")


class TrayOptions:
    default_style = """
    QMenu {
        /* 半透明效果 */
        background-color: rgba(255, 255, 255, 230);
        border: none;
        border-radius: 4px;
    }

    QMenu::item {
        border-radius: 4px;
        /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
        padding: 8px 48px 8px 36px; /* 36px是文字距离左侧距离*/
        background-color: transparent;
    }

    /* 鼠标悬停和按下效果 */
    QMenu::item:selected {
        border-radius: 0px;
        /* 半透明效果 */
        background-color: rgba(232, 232, 232, 232);
    }

    /* 禁用效果 */
    QMenu::item:disabled {
        background-color: transparent;
    }

    /* 图标距离左侧距离 */
    QMenu::icon {
        left: 10px;
    }

    /* 分割线效果 */
    QMenu::separator {
        height: 1px;
        background-color: rgb(232, 236, 243);
    }
    """

    def __init__(self, icon, trigger_func, actions, tooltip=None, style=None):
        self.icon = icon
        self.actions = actions
        self.trigger_func = trigger_func
        self.tooltip = tooltip
        if style:
            self.default_style = style

    def buildTray(self, widget):
        tray = QSystemTrayIcon(widget)
        tray.setIcon(QIcon(self.icon))
        tray.setToolTip(self.tooltip)
        if self.actions:
            menu = QMenu()
            menu.setStyleSheet(self.default_style)
            for opt in self.actions:
                if opt.key == "_menu_separator_":
                    menu.addSeparator()
                    continue

                action = QAction(opt.text, widget)
                if opt.icon:
                    action.setIcon(QIcon(opt.icon))
                action.setEnabled(opt.enable)
                if opt.sub_actions:
                    sub_menu = QMenu(opt.text, menu)
                    for op in opt.sub_actions:
                        sub_action = QAction(op.text, widget)
                        if op.icon:
                            sub_action.setIcon(QIcon(op.icon))
                        sub_action.triggered.connect(partial(self.trigger_func, op.key))
                        sub_menu.addAction(sub_action)
                    menu.addMenu(sub_menu)
                else:
                    action.triggered.connect(partial(self.trigger_func, opt.key))
                    menu.addAction(action)
            tray.setContextMenu(menu)

        tray.activated.connect(lambda: self.trigger_func("activated"))
        tray.show()
        return tray

    @staticmethod
    def build_actions(self, actions, trigger_func, widget):
        if actions:
            menu = QMenu()
            for opt in actions:
                action = QAction(opt.text, widget)
                if opt.icon:
                    action.setIcon(QIcon(opt.icon))
                action.triggered.connect(partial(self.trigger_func, opt.key))
                menu.addAction(action)
                if opt.sub_actions:
                    sub_menu = self.__build_actions(opt.sub_actions, widget)
                    if sub_menu:
                        menu.addMenu(sub_menu)
            return menu


class Options:
    """
    Options for creating Browserwindow
    """
    DEFAULT_HTTP_PORT = 58210

    def __init__(self):
        self._title = "pyqt webview"
        self._width = 800
        self._height = 600
        self._background_color = "#FFFFFF"
        self._frameless = False
        # bind object instance to expose frontend
        self._bind = None
        self._url = None
        self._html = None
        self._debug = False
        self._inspector_port = "12580"
        self._drag_selector = ".pyqtweb-drag"
        self._icon = None
        self._tray = None
        self._before_close_window = None

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def background_color(self) -> str:
        return self._background_color

    @background_color.setter
    def background_color(self, hex_color: str):
        self._background_color = hex_color

    @property
    def frameless(self) -> bool:
        return self._frameless

    @frameless.setter
    def frameless(self, frameless: bool):
        self._frameless = frameless

    @property
    def bind(self) -> None:
        return self._bind

    @bind.setter
    def bind(self, bind):
        self._bind = bind

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    # @property
    # def html(self) -> str:
    #     return self._html
    #
    # @html.setter
    # def html(self, html: str):
    #     self._html = html

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        self._debug = debug

    @property
    def inspector_port(self):
        return self._inspector_port

    @inspector_port.setter
    def inspector_port(self, dev_port):
        self._inspector_port = dev_port

    @property
    def drag_selector(self) -> str:
        return self._drag_selector

    @drag_selector.setter
    def drag_selector(self, drag_class):
        self._drag_selector = drag_class

    @property
    def icon(self) -> str:
        return self._icon

    @icon.setter
    def icon(self, icon: str):
        self._icon = icon

    @property
    def tray(self) -> TrayOptions:
        return self._tray

    @tray.setter
    def tray(self, tray: TrayOptions):
        self._tray = tray

    @property
    def before_close_window(self):
        return self._before_close_window

    @before_close_window.setter
    def before_close_window(self, before_close_window_call):
        self._before_close_window = before_close_window_call


class WindowEvent:
    def __init__(self, window):
        self.window = window

    def WindowSetTitle(self, title):
        self.window.setWindowTitle(title)

    def WindowFullscreen(self, full):
        if full:
            if not self.window.isFullScreen():
                self.window.showFullScreen()
        else:
            if self.window.isFullScreen():
                self.window.showNormal()

    def WindowIsFullscreen(self):
        return self.window.isFullScreen()

    def WindowCenter(self):
        screen = QApplication.desktop().geometry()
        x, y = (screen.width() - self.window.geometry().width()) / 2, (
                screen.height() - self.window.geometry().height()) / 2
        self.window.move(round(x), round(y))

    def WindowShow(self, show):
        if show:
            if self.window.isHidden():
                self.window.show()
        else:
            if not self.window.isHidden():
                self.window.hide()

    def WindowSetSize(self, width, height):
        screen = QApplication.desktop().geometry()
        self.window.setGeometry(round((screen.width() - int(width)) / 2), round((screen.height() - int(height)) / 2),
                                int(width), int(height))

    def WindowGetSize(self):
        return {
            "width": self.window.geometry().width(),
            "height": self.window.geometry().height()
        }

    def WindowSetStayOnTop(self, on):
        self.window.setWindowFlag(Qt.WindowStaysOnTopHint, bool(on))
        self.window.show()

    def WindowMaximized(self):
        if not self.window.isMaximized():
            self.window.showMaximized()

    def WindowIsMaximized(self):
        return self.window.isMaximized()

    def WindowMinimized(self):
        if not self.window.isMinimized():
            self.window.showMinimized()

    def WindowIsMinimized(self):
        return self.window.isMinimized()

    def WindowRestore(self):
        self.window.showNormal()

    def WindowSetOpacity(self, level):
        self.window.setWindowOpacity(float(level))

    def WindowShake(self):

        """
        窗口抖动
        :return:
        """
        target = self.window
        if target.isHidden():
            target.show()
        if target.isMinimized():
            target.showNormal()
        if not target.isActiveWindow():
            target.activateWindow()

        if hasattr(target, '_shake_animation'):
            return

        animation = QPropertyAnimation(target, b'pos', target)
        target._shake_animation = animation
        animation.finished.connect(lambda: delattr(target, '_shake_animation'))

        pos = target.pos()
        x, y = pos.x(), pos.y()
        animation.setDuration(200)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, QPoint(x, y))
        animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        animation.setEndValue(QPoint(x, y))
        animation.start(animation.DeleteWhenStopped)

    def WindowClose(self):
        self.window.close()

    def WindowMessageBox(self, type, title, text, okBtnText, noBtnText):
        type_dict = {
            "info": QMessageBox.Information,
            "question": QMessageBox.Question,
            "warning": QMessageBox.Warning,
            "error": QMessageBox.Critical,
        }
        okBtnText = okBtnText if okBtnText is not None else "ok"
        noBtnText = noBtnText if noBtnText is not None else "cancel"

        if type in type_dict:
            box = QMessageBox(type_dict[type], title, text)
            ok = box.addButton(okBtnText, QMessageBox.YesRole)
            no = box.addButton(noBtnText, QMessageBox.NoRole)
            box.show()
            box.exec_()
            if (box.clickedButton() == ok):
                return "ok"
            else:
                return "cancel"
        else:
            return QMessageBox.about(self.window, title, text)

    def OpenDirectoryDialog(self, title, directory):
        title = "请选择文件夹" if title is not None else title
        return QFileDialog.getExistingDirectory(self.window, title, directory)

    def OpenFileDialog(self, title, directory, filters):
        title = "选择文件" if title is not None else title
        file_filter = 'All Files (*)' if filters is None or filters == "*" else f'Choose Files ({filters.replace(";", " ")})'
        res = QFileDialog.getOpenFileName(self.window, title, directory, file_filter)
        return res[0]

    def OpenMultipleFilesDialog(self, title, directory, filters):
        title = "选择多个文件" if title is not None else title
        file_filter = 'All Files (*)' if filters is None or filters == "*" else f'Choose Files ({filters.replace(";", " ")})'
        res = QFileDialog.getOpenFileNames(self.window, title, directory, file_filter)
        return res[0]

    def SaveFileDialog(self, title, file_path, filters):
        title = "保存文件路径" if title is not None else title
        file_filter = 'All Files (*)' if filters is None or filters == "*" else f'Save Files ({filters.replace(";", " ")})'
        res = QFileDialog.getSaveFileName(self.window, title, file_path, file_filter)
        return res[0]

    def BrowserOpenURL(self, url):
        webbrowser.open(url)

    def ClipboardSetText(self, text):
        try:
            QApplication.clipboard().setText(text)
        except:
            return False
        else:
            return True

    def ClipboardGetText(self):
        try:
            return QApplication.clipboard().text()
        except:
            return ""

    def WindowMove(self, x, y):
        self.window.move(x, y)

    def TrayStartFlash(self):
        self.window.start_tray_flash()

    def TrayStopFlash(self):
        self.window.stop_tray_flash()


class JsBridge(QObject):

    def __init__(self, window):
        super(JsBridge, self).__init__()
        self.window = window

    @pyqtSlot(str, str, str, result=str)
    def Invoke(self, func_name, params, id):
        res = None
        try:
            data = None
            args = json.loads(params)
            if getattr(self.window.options.bind, func_name, None) is not None:
                data = getattr(self.window.options.bind, func_name)(*args.values())
            else:
                print(func_name, *args.values())
                data = getattr(self.window.window_event_bind, func_name)(*args.values())
            res = {
                'code': 0,
                'data': data,
                'message': 'ok',
                'method': func_name,
                'id': id,
            }
        except Exception as e:
            print(e)
            res = {
                'code': 1,
                'data': '',
                'message': f"fail {str(e)}",
                'method': func_name,
                'id': id,
            }
        script = f" window.pyqtweb.Api.Invoke('{func_name}','{id}','{json.dumps(res, ensure_ascii=False)}') "
        return self.window.evaluate_js_trigger.emit(script)


class BrowserWindow(QMainWindow):
    evaluate_js_trigger = pyqtSignal(str)
    window_event_trigger = pyqtSignal(str, str)

    default_html = """
        <!doctype html>
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=0">
            </head>
            <title>PyqtWeb</title>
            <body>
                <h1>Hello PyqtWeb</h1>
                <h5>This page is default html, Please setting html or url</h4>
            </body>
        </html>
    """

    def __init__(self, opts: Options):
        super(BrowserWindow, self).__init__()
        self.options = opts
        self.browser = None
        self.local_server = None
        self.devtools_win = None
        self.js_bridge = JsBridge(self)
        self.channel = QWebChannel()
        self.tray = None
        self.tray_flash_timer = None
        self.tray_visible = True
        self.window_event_bind = WindowEvent(self)
        self.init_main_window()

    def init_main_window(self):

        self.setWindowTitle(self.options.title)
        if self.options.frameless:
            self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(self.options.icon))
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(self.options.background_color))
        self.setPalette(palette)

        # build tray
        if self.options.tray:
            self.tray = self.options.tray.buildTray(self)
            self.tray_flash_timer = QTimer(self, timeout=self.on_tray_flash_icon)

        screen = QApplication.desktop().geometry()
        x, y, w, h = (screen.width() - self.options.width) / 2, (
                screen.height() - self.options.height) / 2, self.options.width, self.options.height
        self.setGeometry(round(x), round(y), w, h)

        if self.options.debug:
            #  dev_tools
            os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = self.options.inspector_port

        self.browser = QWebEngineView()
        self.initSettings()

        if self.options.url is not None:
            if not self.options.url.startswith(('http:', 'https:')):
                # 启动本地服务
                threading.Thread(target=self.__start_local_server, daemon=True).start()
                self.browser.setUrl(QUrl(f"http://127.0.0.1:{self.options.DEFAULT_HTTP_PORT}"))
            else:
                self.browser.setUrl(QUrl(self.options.url))
        elif self.options.html is not None:
            self.browser.setHtml(self.options.html, QUrl(''))
        else:
            self.browser.setHtml(BrowserWindow.default_html, QUrl(''))

        source_code = npo.src + core.src + qwebchannel.src + mouse.src % {'drag_selector': self.options.drag_selector}
        script = QWebEngineScript()
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setSourceCode(source_code)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        self.browser.page().profile().scripts().insert(script)

        self.evaluate_js_trigger.connect(self.on_evaluate_js)
        self.window_event_trigger.connect(self.on_window_event)
        self.setCentralWidget(self.browser)
        self.browser.page().loadFinished.connect(self.on_load_finished)

        self.channel.registerObject('_bridge', self.js_bridge)
        self.browser.page().setWebChannel(self.channel)

    def __start_local_server(self):
        directory = os.path.dirname(self.options.url)
        handler_class = partial(SimpleHTTPRequestHandler, directory=directory)
        server = ThreadingHTTPServer(("127.0.0.1", self.options.DEFAULT_HTTP_PORT), handler_class)
        self.local_server = server
        self.local_server.serve_forever()

    def initSettings(self):
        """
        eg: 初始化设置
        """
        # 获取浏览器默认设置
        settings = self.browser.settings()
        # 设置默认编码utf8
        settings.setDefaultTextEncoding("utf-8")
        # 自动加载图片,默认开启
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        # 自动加载图标,默认开启
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        # 开启js,默认开启
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        # js可以访问剪贴板
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        # js可以打开窗口,默认开启
        # settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows,True)
        # 链接获取焦点时的状态,默认开启
        # settings.setAttribute(QWebEngineSettings.LinksIncludedInFocusChain,True)
        # 本地储存,默认开启
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        # 本地访问远程
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        # 本地加载,默认开启
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        # 监控负载要求跨站点脚本,默认关闭
        # settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled,False)
        # 空间导航特性,默认关闭
        # settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled,False)
        # 支持平超链接属性,默认关闭
        # settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled,False)
        # 使用滚动动画,默认关闭
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        # 支持错误页面,默认启用
        # settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        # 支持插件,默认关闭
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # 支持全屏应用程序,默认关闭
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        # 支持屏幕截屏,默认关闭
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, True)
        # 支持html5 WebGl,默认开启
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        # 支持2d绘制,默认开启
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        # 支持图标触摸,默认关闭
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, True)

    def on_evaluate_js(self, script):
        self.browser.page().runJavaScript(script)

    def notify_frontend_listener(self, event_name, data):
        script = f"window.pyqtweb.EventBus.notify('{event_name}',{json.dumps(data)})"
        self.on_evaluate_js(script)

    def on_load_finished(self):
        # bind window event
        funcs = list_bind_funcs(self.window_event_bind)
        funcList = [{'func': k, 'params': ','.join(v)} for k, v in funcs.items()]
        self.on_evaluate_js(f'window.pyqtweb.Api._create_api({funcList})')

        # bind funcs
        if self.options.bind is not None:
            funcs = list_bind_funcs(self.options.bind)
            funcList = [{'func': k, 'params': ','.join(v)} for k, v in funcs.items()]
            self.on_evaluate_js(f'window.pyqtweb.Api._create_api({funcList})')

        if self.options.debug:
            dev_opt = Options()
            dev_opt.title = 'Web Inspector - {}'.format(self.options.title)
            dev_opt.url = 'http://localhost:{}'.format(self.options.inspector_port)
            dev_opt.width = 800
            dev_opt.height = 400
            dev_win = BrowserWindow(dev_opt)
            dev_win.show()
            self.devtools_win = dev_win

    def closeEvent(self, qclose_event):
        if self.options.before_close_window:
            flag = self.options.before_close_window()
            if flag:
                qclose_event.accept()
            else:
                qclose_event.ignore()
                return
        else:
            qclose_event.accept()

        if self.local_server is not None:
            self.local_server.shutdown()

        if self.devtools_win is not None:
            self.devtools_win.close()
        self.browser.page().deleteLater()

    def dropEvent(self, e) -> None:
        print(e)

    def on_window_event(self, event_name, params):
        pass

    def on_tray_flash_icon(self):
        if self.tray_visible:
            self.tray.setIcon(QIcon(self.options.tray.icon))
        else:
            pix = QPixmap(32,32)
            pix.fill(Qt.transparent)
            self.tray.setIcon(QIcon(pix))
        self.tray_visible = not self.tray_visible

    def start_tray_flash(self):
        if self.tray_flash_timer and not self.tray_flash_timer.isActive():
            self.tray_flash_timer.start(500)

    def stop_tray_flash(self):
        if self.tray_flash_timer and self.tray_flash_timer.isActive():
            self.tray_flash_timer.stop()
            self.tray.setIcon(QIcon(self.options.tray.icon))

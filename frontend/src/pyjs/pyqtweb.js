export function EventOn(eventName, callback) {
    window.pyqtweb.EventBus.register(eventName, callback)
}

export function EventOff(eventName) {
    window.pyqtweb.EventBus.unregister(eventName)
}

export function EventEmit(eventName, data) {
    window.pyqtweb.EventBus.notify(eventName, data)
}

export function WindowSetTitle(title) {
    window.pyqtweb.Api['WindowSetTitle'](title)
}

export function WindowIsFullscreen() {
    return window.pyqtweb.Api['WindowIsFullscreen']()
}

export function WindowFullscreen(full) {
    window.pyqtweb.Api['WindowFullscreen'](full)
}


export function WindowCenter() {
    window.pyqtweb.Api['WindowCenter']()
}

export function WindowShow(show) {
    window.pyqtweb.Api['WindowShow'](show)
}

export function WindowSetSize(width, height) {
    window.pyqtweb.Api['WindowSetSize'](width, height)
}


export function WindowGetSize() {
    return window.pyqtweb.Api['WindowGetSize']()
}

export function WindowSetStayOnTop(on) {
    return window.pyqtweb.Api['WindowSetStayOnTop'](on)
}

export function WindowMaximized() {
    window.pyqtweb.Api['WindowMaximized']()
}

export function WindowIsMaximized() {
    return window.pyqtweb.Api['WindowIsMaximized']()
}

export function WindowMinimized() {
    window.pyqtweb.Api['WindowMinimized']()
}

export function WindowIsMinimized() {
    return window.pyqtweb.Api['WindowIsMinimized']()
}

export function WindowRestore() {
    window.pyqtweb.Api['WindowRestore']()
}

export function WindowSetOpacity(level) {
    window.pyqtweb.Api['WindowSetOpacity'](level)
}


export function WindowShake() {
    window.pyqtweb.Api['WindowShake']()
}


export function WindowMessageBox(type, title, text, okBtnText, noBtnText) {
    return window.pyqtweb.Api['WindowMessageBox'](type, title, text, okBtnText, noBtnText)
}

export function OpenFileDialog(title, dirName, filters = "*") {
    return window.pyqtweb.Api['OpenFileDialog'](title, dirName, filters)
}

export function OpenDirectoryDialog(title, dirName) {
    return window.pyqtweb.Api['OpenDirectoryDialog'](title, dirName)
}

export function OpenMultipleFilesDialog(title, dirName, filters = "*") {
    return window.pyqtweb.Api['OpenMultipleFilesDialog'](title, dirName, filters)
}

export function SaveFileDialog(title, filePath, filters = "*") {
    return window.pyqtweb.Api['SaveFileDialog'](title, filePath, filters)
}

export function BrowserOpenURL(url) {
    window.pyqtweb.Api['BrowserOpenURL'](url)
}

export function ClipboardSetText(text) {
    return window.pyqtweb.Api['ClipboardSetText'](text)
}

export function ClipboardGetText() {
    return window.pyqtweb.Api['ClipboardGetText']()
}

export function WindowClose() {
    window.pyqtweb.Api['WindowClose']()
}

export function TrayStartFlash() {
    window.pyqtweb.Api['TrayStartFlash']()
}

export function TrayStopFlash() {
    window.pyqtweb.Api['TrayStopFlash']()
}
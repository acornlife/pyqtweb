<style>
button {
  margin: 5px;
}
</style>

<template>
  <button type="button" @click="WindowSetTitle('标题' + Math.random().toString().substring(2))">设置标题</button>
  <button type="button" @click="WindowFullscreen(true)">全屏</button>
  <button type="button" @click="WindowFullscreen(false)">取消全屏</button>
  <button type="button" @click="ifFullScreen">是否全屏</button>
  <button type="button" @click="WindowCenter()">窗口居中</button>
  <button type="button" @click="WindowShow(true)">显示窗口</button>
  <button type="button" @click="WindowShow(false)">隐藏窗口</button>
  <button type="button" @click="setWindowSize">设置窗口大小</button>
  <button type="button" @click="getWindowSize">获取窗口大小</button>
  <button type="button" @click="WindowSetStayOnTop(true)">窗口置顶</button>
  <button type="button" @click="WindowSetStayOnTop(false)">窗口取消置顶</button>
  <button type="button" @click="WindowMaximized()">窗口最大化</button>
  <button type="button" @click="WindowMinimized()">窗口最小化</button>
  <button type="button" @click="WindowRestore()">恢复窗口</button>
  <button type="button" @click="windowIsMaximized">窗口是否最大化</button>
  <button type="button" @click="windowIsMinimized">窗口是否最小化</button>
  <button type="button" @click="WindowClose">窗口关闭</button>
  <button type="button" @click="setWindowOpacity">设置窗口透明度</button>
  <button type="button" @click="WindowShake()">窗口抖动</button>
  <button type="button" @click="messagebox">系统弹框</button>
  <button type="button" @click="openDir">打开目录</button>
  <button type="button" @click="openFile">打开文件所在位置</button>
  <button type="button" @click="openMultiFiles">打开多文件</button>
  <button type="button" @click="saveFile">保存文件</button>
  <button type="button" @click="setClipboardText">设置剪贴板</button>
  <button type="button" @click="getClipboardText">读取剪贴板</button>
  <div style="display: inline-block;width: 100px;height: 20px;background: cyan" class="pyqtweb-drag"></div>
    <button type="button" @click="TrayStartFlash()">图标闪烁</button>
    <button type="button" @click="TrayStopFlash()">图标停止闪烁</button>
</template>

<script setup>
import {
  WindowSetTitle,
  WindowFullscreen,
  WindowIsFullscreen,
  WindowCenter,
  WindowShow,
  WindowSetSize,
  WindowGetSize,
  WindowSetStayOnTop,
  WindowMaximized,
  WindowIsMaximized,
  WindowMinimized,
  WindowIsMinimized,
  WindowRestore,
  WindowSetOpacity,
  WindowShake,
  WindowMessageBox,
  OpenDirectoryDialog,
  OpenFileDialog,
  OpenMultipleFilesDialog,
  SaveFileDialog,
  ClipboardGetText,
  ClipboardSetText,
  WindowClose,
  EventOn,
    TrayStartFlash,
    TrayStopFlash
} from "../pyjs/pyqtweb.js"
import {onMounted, ref} from "vue";

const ifFullScreen = function () {
  WindowIsFullscreen().then(res => {
    alert(res)
  })
}

/**
 * 校验只要是数字（包含正负整数，0以及正负浮点数）就返回true
 **/



const setWindowSize = function () {
  let width = window.prompt('请输入窗口宽度')
  let height = window.prompt('请输入窗口高度')
  WindowSetSize(width, height)
}

const getWindowSize = function () {
  WindowGetSize().then(res => {
    alert(`width:${res.width} height:${res.height}`)
  })
}

const windowIsMaximized = function () {
  WindowIsMaximized().then(res => alert(res))
}

const windowIsMinimized = function () {
  WindowIsMinimized().then(res => alert(res))
}

const setWindowOpacity = function () {
  let level = window.prompt('请输入窗口透明度')
  WindowSetOpacity(level)
}

const messagebox = function () {
  let typeSelect = window.prompt("弹框类型：\n1: 信息框\n2：询问框\n3：警告框\n4：错误框 ")
  let title = window.prompt("标题（title）")
  let text = window.prompt("内容（text）")
  let yesText = window.prompt("确定按钮文字")
  let cancelText = window.prompt("取消按钮文字")

  let type = ""
  switch (typeSelect) {
    case "1":
      type = "info";
      break;
    case "2":
      type = "question";
      break;
    case "3":
      type = "warning";
      break;
    case "4":
      type = "error";
      break;
  }
  WindowMessageBox(type, title, text, yesText, cancelText).then(res => alert(res))

}

const openDir = function () {
  let title = "打开文件目录"
  let dirName = "D:/"
  OpenDirectoryDialog(title, dirName).then(res => alert(res))
}

const openFile = function () {
  let title = "打开文件"
  let dirName = "D:/"
  OpenFileDialog(title, dirName).then(res => alert(res))
}
const openMultiFiles = function () {
  let title = "选择多文件"
  let dirName = "D:/"
  let filters = "*.txt;*.py;*.png"
  OpenMultipleFilesDialog(title, dirName, filters).then(res => alert(res))
}

const saveFile = function () {
  let title = "保存文件"
  let dirName = "D:/pyqtweb.txt"
  let filters = "*.txt;"
  SaveFileDialog(title, dirName, filters).then(res => alert(res))
}

const setClipboardText = function () {
  let text = window.prompt("文本内容")
  ClipboardSetText(text)
}

const getClipboardText = function () {
  ClipboardGetText().then(res => alert(res))
}

onMounted(() => {

  // 事件监听
  EventOn('date-change', function (res) {
    alert(res)
  })

})

</script>
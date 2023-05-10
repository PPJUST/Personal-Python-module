# 导入相关的库
import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class DropLabel(QLabel):
    """Qt的QLabel类复写，拖入文件后发送拖入文件的列表信号"""
    dropSignal = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # 设置可拖入

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_path = [url.toLocalFile() for url in urls]  # 获取多个文件的路径的列表
            self.dropSignal.emit(drop_path)  # 发送文件列表信号


class DropLineEdit(QLineEdit):
    """Qt的QLineEdit类复写，拖入文件后将控件文本设置为拖入文件所属的文件夹路径/拖入文件夹的路径"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # 设置可拖入

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()  # 获取路径
            if os.path.isdir(path):
                self.setText(path)
            elif os.path.isfile(path):
                self.setText(os.path.split(path)[0])
                # self.setText(path)

import os

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtWidgets import QTableView, QMessageBox

from .AudioPlayer import AudioPlayerDialog, getSupportAudioFormat
from .Widgets import ProjectViewMenu
from .utils import dumpTempAudio


class ProjectView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QTableView.DragDropMode.DragDrop)
        self.supportFormat =  getSupportAudioFormat()
        print("AudioPlayer",f"supports {self.supportFormat}")

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().endswith(self.supportFormat):
                    event.accept()
                    print(self.__class__.__name__,"dragEnterEvent","accept",url.toLocalFile())
                    return
        event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        event.accept()
        index = self.indexAt(event.position().toPoint())
        if not index.isValid():
            return
            # 获取当前索引所在行
        row = index.row()
        filePath = event.mimeData().urls()[0].toLocalFile()
        try:
            with open(filePath, "rb") as f:
                binaryData = f.read()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"读取文件失败:\n{e}")
            return
        byteArray = QByteArray()
        byteArray.append(binaryData)

        col = self.model().columnCount() - 2
        idx = self.model().index(row, col, index.parent())
        self.addData(idx, byteArray, filePath)

    def addData(self, idx: QtCore.QModelIndex, byteArray: QByteArray, filePath):
        if self.model().data(idx, Qt.ItemDataRole.DisplayRole) not in {"", None}:
            # 如果已存在数据，则弹框询问是否替换
            btn = QMessageBox.question(self, "Replace", "Replace the existing file?",
                                       QMessageBox.StandardButton.Yes,
                                       QMessageBox.StandardButton.No)
            if btn == QMessageBox.StandardButton.Yes:
                self.model().setData(idx, byteArray, Qt.ItemDataRole.EditRole)
                size = byteArray.size()
                if size > 1024 * 1024:
                    size = f"{size / 1024 / 1024:.2f}MB"
                else:
                    size = f"{size / 1024:.2f}KB"
                ext = os.path.splitext(filePath)[1]
                # set data
                self.model().setData(idx, f"{size}", Qt.ItemDataRole.DisplayRole)
                # set data format
                self.model().setData(self.model().index(idx.row(), idx.column() + 1), ext,
                                     Qt.ItemDataRole.EditRole)
                self.model().dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
                print(self.__class__.__name__,f"dropped {filePath} into index:{((idx.row(), idx.column()))},size:{size}")
                return
            else:
                return
        else:
            r = self.model().setData(idx, byteArray, Qt.ItemDataRole.EditRole)
            size = byteArray.size()
            if size > 1024 * 1024:
                size = f"{size / 1024 / 1024:.2f}MB"
            else:
                size = f"{size / 1024:.2f}KB"
            ext = os.path.splitext(filePath)[1]
            # set data
            self.model().setData(idx, f"{size}", Qt.ItemDataRole.DisplayRole)
            # set data format
            self.model().setData(self.model().index(idx.row(), idx.column() + 1), ext,
                                 Qt.ItemDataRole.EditRole)
            self.model().dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            # r = r and self.model().setData(idx, f"存在数据:{size:.2f}MB", Qt.ItemDataRole.DisplayRole)
            if r:
                print(self.__class__.__name__,f"dropped {filePath} into index:{(idx.row(), idx.column())},size:{size}MB")
            else:
                print(self.__class__.__name__,"failed")
            return

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        # 获取鼠标位置的索引
        index = self.indexAt(e.pos())
        display, data, dialogue, _ = self.getRowInfo(index)
        if display not in ("", None):
            tempF = dumpTempAudio(data[0], data[1])
            apd = AudioPlayerDialog(dialogue, tempF, self)
            apd.finished.connect(lambda r: {
                print(self.__class__.__name__,f"AudioPlayerDialog finished with {r}"),
                os.remove(tempF)
            })
            apd.exec()
        else:
            QMessageBox.information(self, "行-双击事件", "当前行没有存放音频,无法快捷使用双击播放")
        super().mouseDoubleClickEvent(e)

    def dragLeaveEvent(self, e: QtGui.QDragLeaveEvent) -> None:
        print(self.__class__.__name__,"dragLeaveEvent")
        super().dragLeaveEvent(e)

    def startDrag(self, supportedActions: QtCore.Qt.DropAction) -> None:
        print("startDrag")
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setData("text/plain", QByteArray(b'6'))
        drag.setMimeData(mimeData)

        drag.exec(supportedActions | Qt.DropAction.CopyAction)
        super().startDrag(supportedActions)

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent) -> None:
        print("contextMenuEvent")
        # 获取当前鼠标位置
        pos = a0.pos()
        # 获取当前鼠标位置的索引
        index = self.indexAt(pos)
        display, data, dialogue, pk = self.getRowInfo(index)

        menu = ProjectViewMenu(self)
        if display not in ("", None):
            menu.addVoiceAction.setDisabled(True)
            menu.execAction(self.mapToGlobal(pos), index, data, dialogue, pk)
        else:
            menu.deleteVoiceAction.setDisabled(True)
            menu.exportVoiceAction.setDisabled(True)
            menu.playVoiceAction.setDisabled(True)
            menu.execAction(self.mapToGlobal(pos), index)

        super().contextMenuEvent(a0)

    def getRowInfo(self, index):
        row = index.row()
        column = self.model().columnCount()
        display = self.model().data(self.model().index(row, column - 2), Qt.ItemDataRole.DisplayRole)
        data = self.model().data(self.model().index(row, column - 2), Qt.ItemDataRole.EditRole)
        dataFormat = self.model().data(self.model().index(row, column - 1), Qt.ItemDataRole.EditRole)
        # 获取表头“Dialogue”的索引
        dialogue = self.model().data(self.model().index(row, 3), Qt.ItemDataRole.DisplayRole)
        primaryKey = self.model().getRowPrimaryKey(row)

        return display, (data, dataFormat), dialogue, primaryKey

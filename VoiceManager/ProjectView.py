import os

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtWidgets import QTableView, QMessageBox

from .AudioPlayer import AudioPlayerDialog
from .Widgets import ProjectViewMenu
from .utils import dumpTempAudio, get_extension


class ProjectView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QTableView.DragDropMode.DragDrop)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            if event.mimeData().urls()[0].toLocalFile().endswith(("wav", "mp3", "ogg", "m4a")):
                event.accept()
                print("dragEnterEvent", "accept")
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        event.accept()
        # super().dropEvent(event)
        #
        # if event.mimeData().hasUrls():
        #     filenames = [url.toLocalFile() for url in event.mimeData().urls()]
        #     event.accept()
        #     print(filenames)
        #     # self.table_model.addAudioFiles(filenames)
        # 从鼠标获取当前的索引
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

        col = self.model().columnCount() - 1
        idx = self.model().index(row, col, index.parent())
        self.addData(idx, byteArray, filePath)


    def addData(self,idx:QtCore.QModelIndex,byteArray:QByteArray,filePath):
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
                ext = get_extension(byteArray[:4].data())[1:]
                self.model().setData(idx, f"{ext} {size}", Qt.ItemDataRole.DisplayRole)
                self.model().dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
                print(f"dropped {filePath} into index:{((idx.row(), idx.column()))},size:{size:.2f}MB")
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
            ext = get_extension(byteArray[:4].data())[1:]
            self.model().setData(idx,f"{ext} {size}",Qt.ItemDataRole.DisplayRole)
            self.model().dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            # r = r and self.model().setData(idx, f"存在数据:{size:.2f}MB", Qt.ItemDataRole.DisplayRole)
            if r:
                print(f"dropped {filePath} into index:{(idx.row(), idx.column())},size:{size}MB")
            else:
                print("failed")
            return
    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        # 获取鼠标位置的索引
        index = self.indexAt(e.pos())
        display, data, dialogue,_ = self.getRowInfo(index)
        if display not in ("", None):
            tempF = dumpTempAudio(data, get_extension(data))
            apd = AudioPlayerDialog(dialogue, tempF, self)
            apd.finished.connect(lambda r: {
                print(f"AudioPlayerDialog finished with {r}"),
                os.remove(tempF)
            })
            apd.exec()
        else:
            QMessageBox.information(self, "行-双击事件", "当前行没有存放音频,无法快捷使用双击播放")
        super().mouseDoubleClickEvent(e)
            
        

    def dragLeaveEvent(self, e: QtGui.QDragLeaveEvent) -> None:
        print("dragLeaveEvent")
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
        display, data, dialogue,pk = self.getRowInfo(index)

        menu = ProjectViewMenu(self)
        if display not in ("", None):
            menu.addVoiceAction.setDisabled(True)
            menu.execAction(self.mapToGlobal(pos),index, data.data(),dialogue,pk)
        else:
            menu.deleteVoiceAction.setDisabled(True)
            menu.exportVoiceAction.setDisabled(True)
            menu.playVoiceAction.setDisabled(True)
            menu.execAction(self.mapToGlobal(pos),index)

        super().contextMenuEvent(a0)
    
    def getRowInfo(self,index):
        row = index.row()
        column = self.model().columnCount()
        display = self.model().data(self.model().index(row, column - 1), Qt.ItemDataRole.DisplayRole)
        data = self.model().data(self.model().index(row, column - 1), Qt.ItemDataRole.EditRole)
        # 获取表头“Dialogue”的索引
        dialogue = self.model().data(self.model().index(row, 3), Qt.ItemDataRole.DisplayRole)
        primaryKey = self.model().getRowPrimaryKey(row)

        return display,data,dialogue,primaryKey

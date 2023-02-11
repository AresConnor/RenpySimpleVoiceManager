import os
from typing import Tuple

from PySide6 import QtWidgets
from PySide6.QtCore import QByteArray, QModelIndex, Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox

from .AudioPlayer import AudioPlayerDialog
from .utils import dumpTempAudio


class ProjectViewMenu(QtWidgets.QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.playVoiceAction = self.addAction("播放音频")
        self.deleteVoiceAction = self.addAction("删除音频")
        self.addVoiceAction = self.addAction("添加音频")
        self.exportVoiceAction = self.addAction("导出音频")

    def execAction(self, pos, index: QModelIndex, data: Tuple[bytes, str] = ..., dialogue=..., pk=...):
        action = self.exec(pos)
        if action == self.playVoiceAction:
            tempF = dumpTempAudio(data[0], data[1])
            apd = AudioPlayerDialog(dialogue, tempF, self.parent)
            apd.finished.connect(lambda r: {
                print(self.__class__.__name__,f"AudioPlayerDialog finished with {r}"),
                os.remove(tempF)
            })
            apd.exec()

        elif action == self.deleteVoiceAction:
            idx = self.parent.model().index(index.row(), self.parent.model().columnCount() - 2)
            r = self.parent.model().setData(idx, QByteArray(), Qt.ItemDataRole.EditRole)
            # set data format
            self.parent.model().setData(self.parent.model().index(idx.row(), idx.column() + 1), "",
                                        Qt.ItemDataRole.EditRole)
            self.parent.model().dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            if not r:
                QMessageBox.critical(self, "错误", f"删除音频失败")
                return
            print(self.__class__.__name__,"deleteVoiceAction")

        elif action == self.addVoiceAction:
            name, _ = QFileDialog.getOpenFileName(self.parent, "添加音频", "", "音频文件 (*.wav *.mp3 *.ogg *.m4a)")
            try:
                with open(name, "rb") as f:
                    binaryData = f.read()
            except Exception as e:
                QMessageBox.warning(self, "错误", f"读取文件失败:\n{e}")
                return
            byteArray = QByteArray()
            byteArray.append(binaryData)
            col = self.parent.model().columnCount() - 2
            idxData = self.parent.model().index(index.row(), col, index.parent())
            self.parent.addData(idxData, byteArray, name)
        elif action == self.exportVoiceAction:
            binaryData, ext = data
            col = self.parent.model().columnCount() - 1
            # idx = self.parent.model().index(index.row(), col, index.parent())
            default_fn = os.path.join(os.getcwd(), f"{pk}{ext}")
            name, _ = QFileDialog.getSaveFileName(self.parent, "导出音频", f"{default_fn}", f"音频文件 (*{ext})")
            if name != '':
                try:
                    with open(name, "wb") as f:
                        f.write(binaryData)
                        QMessageBox.information(self, "成功", f"导出文件成功:\n{name}")
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"导出文件失败:\n{e}")
                    return
            print(self.__class__.__name__,"exportVoiceAction")

        return action

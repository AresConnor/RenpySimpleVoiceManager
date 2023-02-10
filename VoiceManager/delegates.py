from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class ProjectViewDelegate(QStyledItemDelegate):

    def __init__(self, view: QtWidgets.QAbstractItemView):
        super().__init__()
        self.binary_data = None
        self.mime_data = None
        self.view = view

    def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option: QStyleOptionViewItem,
                    index: QtCore.QModelIndex) -> bool:
        # 如果event是dragEnterEvent
        # if event.type() == QtCore.QEvent.Type.DragEnter:
        #     # 如果是音频文件
        #     if event.mimeData().urls()[0].toLocalFile().endswith(".ogg", ".wav", ",mp3", ".m4a"):
        #         # 接受拖拽
        #         event.accept()
        #         return True
        #     else:
        #         event.ignore()
        #         return False
        #
        # elif event.type() == QtCore.QEvent.Type.DragMove:
        #     # 如果鼠标超出了程序框
        #     if not option.rect.contains(event.pos()):
        #         # 构建data
        #         mime_data = QtCore.QMimeData()
        #         # 从该index的最后一列获取数据
        #         binary_data = model.data(model.index(index.row(), model.columnCount() - 1))
        #         mime_data.setData("application/binary", binary_data)
        #         # 构建拖拽事件
        #         drag = QtGui.QDrag(self.view)
        #         drag.setMimeData(mime_data)
        #         # 开始拖拽
        #
        #
        # elif event.type() == QtCore.QEvent.Type.DragLeave:
        #     # 从该index的最后一列获取数据
        #     binary_data = model.data(model.index(index.row(), model.columnCount() - 1))
        #     # 如果数据为空
        #     if binary_data in {b"", None}:
        #         # 忽略该事件
        #         event.ignore()
        #         return False
        #     return True
        #
        #     pass
        # elif event.type() == QtCore.QEvent.Type.Drop:
        #     event.accept()
        #     if event.mimeData().urls()[0].toLocalFile().endswith(".ogg", ".wav", ",mp3", ".m4a"):
        #         event.accept()
        #         # 检查该index下最后一列是否有数据
        #         if model.data(model.index(index.row(), model.columnCount() - 1)) in {b"", None}:
        #             # 如果没有数据,则将拖拽的文件的数据写入该index下最后一列
        #             model.setData(model.index(index.row(), model.columnCount() - 1), self.binary_data)
        #             return True
        #         else:
        #             # 如果已存在数据，则弹框询问是否替换
        #             btn = QMessageBox.question(self.view, "Replace", "Replace the existing file?",
        #                                        QMessageBox.StandardButton.Yes,
        #                                        QMessageBox.StandardButton.No)
        #             if btn == QMessageBox.StandardButton.Yes:
        #                 mime_data = event.mimeData()
        #                 binary_data = mime_data.data("application/binary")
        #                 model.setData(model.index(index.row(), model.columnCount() - 1), self.binary_data)
        #                 return True
        #             else:
        #                 return False
        #     elif event.type() == QtCore.QEvent.Type.MouseButtonPress:
        #         # 如果当前行最后一行有数据
        #         self.binary_data = model.data(model.index(index.row(), model.columnCount() - 1))
        #         if self.binary_data not in {b"", None}:
        #             QDrag = QtGui.QDrag(self.view)
        #             self.mime_data = QtCore.QMimeData()
        #             self.mime_data.setData("application/binary", self.binary_data)
        #             QDrag.setMimeData(self.mime_data)
        #             QDrag.exec()
        return super().editorEvent(event, model, option, index)

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        super().paint(painter, option, index)

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable|Qt.ItemFlag.ItemIsDropEnabled

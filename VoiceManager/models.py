import typing

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtSql import QSqlTableModel, QSqlQuery, QSqlDatabase



def get_mime_type(binary_data):
    magic_numbers = {
        b'OggS': 'audio/ogg',
        b'RIFF': 'audio/wav',
        b'\x49\x44\x33': 'audio/mpeg',
        b'\x00\x00\x00\x18': 'audio/mp4',
    }
    header = binary_data[:4]
    mime_type = magic_numbers.get(header, None)
    return mime_type


class MySqlTableModel(QSqlTableModel):

    def __init__(self, proj, parent: typing.Optional[QtCore.QObject] = ..., db: QSqlDatabase = ...) -> None:
        super().__init__(parent=None, db=db)
        self.proj = proj
        # 寻找PRIMARY KEY
        headers = self.proj.projSettings["dataBase"]["headers"]
        for header in headers:
            if header["type"].find("PRIMARY KEY") != -1:
                self.primaryKey = header["name"]
                break

    def flags(self, index):
        if index.column() in range(self.columnCount() - 2):
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDropEnabled
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled

    def data(self, idx: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole and idx.column() == (self.columnCount() - 2):
            # 如果索引处在最后一列，且role为DisplayRole,代表是Blob类型的显示
            byteArray = super().data(idx, Qt.ItemDataRole.EditRole)
            if byteArray != '':
                byteArray: QByteArray
                size = byteArray.size()
                if size > 1024 * 1024:
                    size = f"{size / 1024 / 1024:.2f}MB"
                else:
                    size = f"{size / 1024:.2f}KB"
                return f"{size}"
        if role is not ...:
            return super().data(idx, role)

    def setData(self, index: QtCore.QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.ItemDataRole.DisplayRole:
            # 将显示的值改成value
            return super().setData(index, value, Qt.ItemDataRole.DisplayRole)
        elif role == Qt.ItemDataRole.EditRole:
            if index.column() == self.columnCount() - 2:
                self.database().transaction()
                query = QSqlQuery(db=self.database())
                query.prepare(
                    f"UPDATE {self.tableName()} SET {self.headerData(index.column(), Qt.Orientation.Horizontal)} = :blobData WHERE {self.primaryKey} = :id")
                query.bindValue(":blobData", value)
            else:
                self.database().transaction()
                query = QSqlQuery(db=self.database())
                query.prepare(
                    f"UPDATE {self.tableName()} SET {self.headerData(index.column(), Qt.Orientation.Horizontal)} = :textData WHERE {self.primaryKey} = :id")
                query.bindValue(":textData", value)

            primaryKeyValue = self.getRowPrimaryKey(index.row())
            query.bindValue(":id", primaryKeyValue)
            # 执行sql语句
            print(self.__class__.__name__,value[:100], primaryKeyValue)
            result = query.exec()
            print(self.__class__.__name__,f"{self.database().isOpen()=}, {query.executedQuery()=}, {query.lastError().text()=}")
            print(self.__class__.__name__,f'{query.numRowsAffected()=}')
            # 提交事务
            if result:
                print(self.__class__.__name__,query.executedQuery())
                self.database().commit()
                query.exec(f"select VoiceFile from ScriptTable where {primaryKeyValue} = {primaryKeyValue}")
                return True
            else:
                self.database().rollback()
                print(self.__class__.__name__,f"setData failed:{query.lastError().text()}")
                return False

    def mimeTypes(self) -> typing.List[str]:
        print(self.__class__.__name__,"mimeTypes")
        return ["application/binary"]

    def getRowPrimaryKey(self, row):
        primaryKeyColumn = self.record().indexOf(self.primaryKey)
        # 获取主键的值
        return self.data(self.index(row, primaryKeyColumn), Qt.ItemDataRole.DisplayRole)

    def mimeData(self, indexes: typing.List[QtCore.QModelIndex]) -> QtCore.QMimeData:
        print(self.__class__.__name__,[(index.row(), index.column()) for index in indexes if index.isValid()])
        return super().mimeData(indexes)


    def supportedDropActions(self) -> Qt.DropAction:
        return Qt.DropAction.CopyAction

    def canDropMimeData(self, data: QtCore.QMimeData, action: Qt.DropAction, row: int, column: int,
                        parent: QtCore.QModelIndex) -> bool:
        return True

import csv
import os.path
import shutil

from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

default_project_settings = {
    "dataBase": {
        "type": "sqlite",
        "path": "",
        "table_name": "ScriptTable",
        "headers": [
            {
                "name": "Identifier",
                "type": "TEXT"

            },
            {
                "name":"Character",
                "type":"TEXT"
            },
            {
                "name":"Dialogue",
                "type":"TEXT"
            },
            {
                "name":"Filename",
                "type":"TEXT"

            },
            {
                "name":"LineNumber",
                "type":"TEXT"
            },
            {

                "name": "RenPyScript",
                "type": "TEXT"
            },

        ]
    },
    "info": {
        "dataBase": "do not modifier headers,unless Renpy officially changed the format of the exported dialogue file."
    }
}


def readTabFile(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        cols = [column for column in csv.reader(f, delimiter='\t')]
        headColumn = cols[0]
        dataColumns = cols[1:]

    return headColumn, dataColumns


def readDBFile(fileName):
    pass


class Project:
    def __init__(self, projName, projSettings=None):
        self.projName = projName
        self.sqlDatabaseModel:QSqlTableModel
        self.projSettings: dict = projSettings or default_project_settings
        self._initDataBase()


    def remove(self):
        self._closeDataBase()
        shutil.rmtree(f'Projects/{self.projName}')

    def _initDataBase(self):
        if self.projSettings["dataBase"]["type"] == "sqlite":
            self.sqlDatabase = QSqlDatabase().addDatabase("QSQLITE")
            self._ensureWorkingDirectory()
            self.sqlDatabase.setDatabaseName(self.projSettings["dataBase"]["path"] if self.projSettings["dataBase"][
                "path"] else f"Projects/{self.projName}/dataBase.db")
            self.sqlDatabase.open()
            # 检查表self.projSettings['dataBase']['table_name']是否存在
            if not self.sqlDatabase.tables().__contains__(self.projSettings['dataBase']['table_name']):
                # 表不存在，创建表
                self.sqlQuery = QSqlQuery(self.sqlDatabase)
                _sql = f"CREATE TABLE {self.projSettings['dataBase']['table_name']} ("
                _sql += ', '.join([f'{headerData["name"]} {headerData["type"]}' for headerData in self.projSettings['dataBase']['headers']])
                _sql += ")"
                self.sqlQuery.exec(_sql)
                print(self.sqlQuery.lastQuery(),self.sqlQuery.lastError().text())
            self.sqlDatabaseModel = QSqlTableModel(db=self.sqlDatabase)
            self.sqlDatabaseModel.setTable(self.projSettings['dataBase']['table_name'])


        elif self.projSettings["dataBase"]["type"] == "mysql":
            pass
        else:
            raise ValueError("Unsupported database type")

    def database(self):
        return self.sqlDatabase

    def model(self):
        return self.sqlDatabaseModel

    def dataBaseInsertData(self, data: list):
        _sql = f"INSERT INTO {self.projSettings['dataBase']['table_name']} VALUES ({', '.join(['?' for _ in range(len(data))])})"
        # 预备sql语句
        self.sqlQuery.prepare(_sql)
        for _data in data:
            self.sqlQuery.addBindValue(_data)
        self.sqlQuery.exec()
        # 检查是否插入成功
        if self.sqlQuery.lastError().isValid():
            print(self.sqlQuery.lastError().text())
            return False
        return True


    def _closeDataBase(self):
        if self.sqlDatabase.isOpen():
            self.sqlDatabase.close()

    def _ensureWorkingDirectory(self):
        if not os.path.exists(f'Projects/{self.projName}'):
            os.mkdir(f'Projects/{self.projName}')
            return True
        else:
            return False
    def __del__(self):
        self._closeDataBase()

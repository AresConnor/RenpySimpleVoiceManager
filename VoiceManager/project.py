import json
import os
import shutil

from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QDialog

from . import VMMainWindow
from .models import MySqlTableModel
from .ui.ProjectDialog import ProjectUI
from .utils import default_project_settings


class Project:
    def __init__(self, projName, projSettings=None):
        self.projName = projName
        self.delegates = None
        self.sqlDatabaseModel: QSqlTableModel
        self.projSettings: dict = projSettings or default_project_settings
        self._initDataBase()
        self.status = {}
        self.voiceColumnName = self.projSettings['dataBase']['headers'][-1]['name']

    def close(self):
        self.save()
        self._closeDataBase()

    def save(self):
        # 读取Projects.json
        with open("Projects/Projects.json", "r", encoding="utf-8") as f:
            projects = json.load(f)
        # 更新项目信息
        projects.update({self.projName: self.projSettings})
        # 写入Projects.json
        with open("Projects/Projects.json", "w", encoding="utf-8") as f:
            json.dump(projects, f, ensure_ascii=False, indent=4)
        # 提交所有事务
        self.sqlDatabase.commit()

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
                _sql += ', '.join([f'{headerData["name"]} {headerData["type"]}' for headerData in
                                   self.projSettings['dataBase']['headers']])
                _sql += ")"
                self.sqlQuery.exec(_sql)
                print(self.__class__.__name__,self.sqlQuery.lastQuery(), self.sqlQuery.lastError().text())
            self.sqlDatabaseModel = MySqlTableModel(self, db=self.sqlDatabase)
            self.sqlDatabaseModel.setTable(self.projSettings['dataBase']['table_name'])

        elif self.projSettings["dataBase"]["type"] == "mysql":
            pass
        else:
            raise ValueError("Unsupported database type")

    def open(self):
        self._initDataBase()

    def isOpen(self):
        return self.sqlDatabase.isOpen()

    def database(self):
        return self.sqlDatabase

    def getDBTotalNum(self, _filter):
        if _filter != '':
            _filter = _filter[:-1]
        query = QSqlQuery()
        currentTableName = self.status.get('currentTableName', self.projSettings['dataBase']['table_name'])
        query.exec(f"SELECT COUNT(*) FROM {currentTableName} {_filter}")
        query.first()
        return query.value(0)

    def model(self):
        return self.sqlDatabaseModel

    def dataBaseInsertData(self, data: list):
        query = QSqlQuery(self.sqlDatabase)
        _sql = f"INSERT INTO {self.projSettings['dataBase']['table_name']} VALUES ({', '.join(['?' for _ in range(len(data))])})"
        # 预备sql语句
        query.prepare(_sql)
        for _data in data:
            query.addBindValue(_data)
        query.exec()
        # 检查是否插入成功
        if query.lastError().isValid():
            print(self.__class__.__name__,query.lastError().text())
            return False
        # 为了让model更新数据，需要调用select()方法
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


class ProjectDialog(QDialog):
    def __init__(self, parent: VMMainWindow):
        super().__init__(parent=parent)
        self.parent = parent
        self.projectListModel = QStringListModel()
        self.projects = None
        self.selectedProject = None
        self.ui = ProjectUI()
        self.ui.setupUi(self)
        self.ui.projectListView.setModel(self.projectListModel)

        self.ui.openProjBtn.setEnabled(False)
        self.ui.delProjBtn.setEnabled(False)

        self.ui.projectListView.pressed.connect(self.onProjectListViewPressed)

        self.ui.projectListView.doubleClicked.connect(self.onOpenProjBtnClicked)
        self.ui.openProjBtn.clicked.connect(self.onOpenProjBtnClicked)

        self.ui.delProjBtn.clicked.connect(self.onDelProjBtnClicked)

        # self.ui.openProjBtn.clicked.connect(self.openProject)

    def onOpenProjBtnClicked(self):
        self.parent.projectReadySignal.emit(self.parent.projects[self.selectedProject])
        self.hide()

    def onDelProjBtnClicked(self):
        workingProject = self.parent.workingProject
        # 如果要删除的是当前项目
        if workingProject is not None and workingProject.projName == self.selectedProject:
            # 先关闭当前项目
            self.parent.closeWorkingProject()
            # 删除项目
            self.parent.projects.pop(self.selectedProject).remove()
        else:
            # 删除项目
            self.parent.projects.pop(self.selectedProject).remove()
        # 保存Projects.json
        with open("Projects/Projects.json", "w", encoding='utf-8') as f:
            json.dump({projObj.projName: projObj.projSettings for projObj in self.parent.projects.values()}, f,
                      indent=4,
                      ensure_ascii=False, sort_keys=True)
        # 更新项目列表
        projNames = self.getProjects()
        self.projectListModel.setStringList(projNames)
        print(self.__class__.__name__,f"Project {self.selectedProject} removed")

    def onProjectListViewPressed(self, index):
        self.ui.openProjBtn.setEnabled(True)
        self.ui.delProjBtn.setEnabled(True)
        self.selectedProject = self.projectListModel.data(index, Qt.ItemDataRole.DisplayRole)

    def show(self) -> None:
        projNames = self.getProjects()
        self.projectListModel.setStringList(projNames)
        super().show()

    def getProjects(self) -> list[str]:
        # 从Projects.json中读取所有项目
        self.projects = {}
        if os.path.exists('Projects/Projects.json'):
            with open('Projects/Projects.json', 'r', encoding='utf-8') as f:
                self.projects = json.load(f)
                return list(self.projects.keys())
        else:
            self.projects = {}
            return []

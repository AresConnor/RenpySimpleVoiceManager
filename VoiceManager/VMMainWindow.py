from PyQt6 import uic, QtGui
from PyQt6.QtCore import QCoreApplication, pyqtSignal, pyqtSlot, Qt, QByteArray, QModelIndex
from PyQt6.QtSql import QSqlQuery, QSqlTableModel
from PyQt6.QtWidgets import QMainWindow, QProgressDialog, QTableView
import json
import os
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from External_tianxi_renpy_Redo.tools.VoiceManager.utils import readTabFile, Project


class VMMainWindow(QMainWindow):
    projectReadySignal = pyqtSignal(Project)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        # 保存Projects.json
        with open("Projects/Projects.json", "w") as f:
            json.dump({projObj.projName: projObj.projSettings for projObj in self.projects.values()}, f, indent=4,
                      ensure_ascii=False, sort_keys=True)

    def __init__(self):
        super().__init__()
        self.workingProject = None
        uic.loadUi("./VoiceManager/main.ui", self)
        self.projects: dict[str, Project] = {}
        self.diffFileActions = {}

        self.initProjects()
        self.initWidgets()

    def initMenus(self) -> None:
        # 初始化菜单栏
        # 1.fileMenu
        self.actionOpen: QAction
        self.actionSave: QAction
        self.initFileActions()
        self.actionOpen.triggered.connect(self.onOpenFile)
        self.actionSave.triggered.connect(self.onSaveFile)
        self.actionOpenProject.triggered.connect(self.onOpenProject)

    def initProjects(self) -> None:
        # 初始化项目列表
        # 打开Projects/Projects.json,如果没有，则创建
        if not os.path.exists("Projects/Projects.json"):
            if not os.path.exists("Projects"):
                os.mkdir("Projects")
            with open("Projects/Projects.json", "w") as f:
                f.write("{}")
        # 读取Projects.json
        with open("Projects/Projects.json", "r") as f:
            projects = json.load(f)
        self.projects = {projName: Project(projName, projSettings) for projName, projSettings in projects.items()}

    def initWidgets(self) -> None:
        self.initMenus()

        self.searchTextEdit.textChanged.connect(self.onSearchTextChanged)
        self.searchTextEdit.setDisabled(False)
        # 初始化窗口函数
        self.projectReadySignal.connect(self.onProjectReady)
        # 设置tableview样式
        self.sqlView: QTableView
        self.sqlView.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sqlView.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    def onOpenFile(self) -> None:
        _filter = ""
        for k in self.diffFileActions.keys():
            _filter += k + ";;"
        _filter = _filter[:-2]
        fileName, fi1ter = QFileDialog.getOpenFileName(filter=_filter)
        if fileName != '':
            self.diffFileActions[fi1ter](fileName)

    @pyqtSlot(Project)
    def onProjectReady(self, project) -> None:
        self.workingProject = project
        self.sqlView: QTableView
        if self.workingProject is not None:
            self.searchTextEdit.setDisabled(True)
            self.sqlView.setModel(project.sqlDatabaseModel)
            self.sqlView.resizeColumnsToContents()
            self.sqlView.resizeRowsToContents()
            self.sqlView.horizontalHeader().setStretchLastSection(True)
            self.sqlView.verticalHeader().setStretchLastSection(True)
            QCoreApplication.processEvents()

    def onSearchTextChanged(self, text: str) -> None:
        pass

    def onSaveFile(self):
        pass

    def initFileActions(self) -> None:

        self.diffFileActions = {
            "制表文件 (*.tab)": self.createNewProject,
            "数据库 (*.db)": lambda _, fileName: print("暂未实现")
        }

    def createNewProject(self, fileName) -> None:
        head, data = readTabFile(fileName)
        projName, received = QInputDialog.getText(self, "创建新项目...", "请输入项目名")
        if received:
            # 判断是否已经存在同名工程
            if projName in self.projects.keys():
                # 弹出选择对话框
                button = QMessageBox.warning(self, "正在创建工程...", f"已存在同名工程{projName},是否覆盖工程",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if button == QMessageBox.StandardButton.Yes:
                    try:
                        self.projects.pop(projName).remove()
                    except Exception as e:
                        QMessageBox.critical(self, "错误", f"删除工程{projName}时出现错误{e}")
                        self.projects
                        return None
                    projObj = Project(projName)
                    self.projects.update({projName: projObj})
                else:
                    return None

            else:
                projObj = Project(projName)
                self.projects.update({projName: projObj})

            progressDialog = QProgressDialog("正在导入数据...", "取消", 0, len(data))
            progressDialog.setWindowFlag(
                Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
            progressDialog.setWindowModality(Qt.WindowModality.WindowModal)
            progressDialog.show()
            i = 0
            for _data in data:
                # _data.append(QByteArray())
                projObj.dataBaseInsertData(_data)
                i += 1
                progressDialog.setValue(i)
                QCoreApplication.processEvents()
                if progressDialog.wasCanceled():
                    projObj.remove()
                    self.projects.pop(projName)
                    return None
            progressDialog.setValue(len(data))

            # 保存Projects.json
            with open("Projects/Projects.json", "w") as f:
                json.dump({projObj.projName: projObj.projSettings for projObj in self.projects.values()}, f,
                          ensure_ascii=False, sort_keys=True, indent=4)

            self.projectReadySignal.emit(projObj)

            return None
        else:
            return None

    def onOpenProject(self) -> None:
        projName, received = QInputDialog.getItem(self, "打开项目...", "请选择项目", self.projects.keys(), 0, False,
                                                  Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        if received:
            self.projectReadySignal.emit(self.projects[projName])
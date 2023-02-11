import json
import os

from PySide6 import QtGui
from PySide6.QtCore import QCoreApplication, Signal, Slot
from PySide6.QtGui import Qt
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from PySide6.QtWidgets import QMainWindow, QProgressDialog, QTableView

from .delegates import ProjectViewDelegate
from .project import Project, ProjectDialog
from .ui.ui import Ui_MainWindow
from .utils import readTabFile, SearchText, loadCharaDefine, translateCharacter


class VMMainWindow(QMainWindow):
    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        print(self.__class__.__name__,"dropEvent")
        a0.accept()
        super().dropEvent(a0)

    projectReadySignal = Signal(Project)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        self.closeWorkingProject()
        # 检查是否有未保存的项目
        for proj in self.projects.values():
            if proj.isOpen():
                proj.close()

    def __init__(self):
        super().__init__()
        self.projectsWindow = None
        self.workingProject = None
        # uic.loadUi("./VoiceManager/main.ui", self)
        self.projects: dict[str, Project] = {}
        self.diffFileActions = {}

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        self.initProjects()
        self.initWidgets()
        self.initProjectsWindow()
        self.charaDefine = loadCharaDefine()

    def initMenus(self) -> None:
        # 初始化菜单栏
        # 1.fileMenu
        self.initFileActions()
        self.ui.actionOpen.triggered.connect(self.onOpenFileActionTriggered)
        self.ui.actionOpenProject.triggered.connect(self.onOpenProjectActionTriggered)
        self.ui.actionProjects.triggered.connect(self.onProjectsActionTriggered)
        self.ui.actionSaveProject.triggered.connect(self.onSaveProjectActionTriggered)
        self.ui.actionusage.triggered.connect(self.onUsageActionTriggered)

    def initProjects(self) -> None:
        # 初始化项目列表
        # 打开Projects/Projects.json,如果没有，则创建
        if not os.path.exists("Projects/Projects.json"):
            if not os.path.exists("Projects"):
                os.mkdir("Projects")
            with open("Projects/Projects.json", "w", encoding='utf-8') as f:
                f.write("{}")
        # 读取Projects.json
        with open("Projects/Projects.json", "r", encoding='utf-8') as f:
            projects = json.load(f)
        self.projects = {projName: Project(projName, projSettings) for projName, projSettings in projects.items()}

    def initWidgets(self) -> None:

        self.initMenus()
        self.ui.searchTextEdit.setDisabled(False)
        self.ui.searchModeBox.addItems(SearchText.getSearchModeTranslationList())
        # 初始化窗口函数
        self.projectReadySignal.connect(self.onProjectReady)
        # 设置tableview样式
        self.ui.sqlView.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.sqlView.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        # 设置tableview底部不吸附
        self.ui.sqlView.verticalHeader().setStretchLastSection(False)
        self.ui.sqlView.setAcceptDrops(True)
        d = ProjectViewDelegate(self.ui.sqlView)
        self.ui.sqlView.setItemDelegate(d)
        # 将检索栏的所有小部件设置为禁用
        self.ui.groupBox.setEnabled(False)

        self.ui.lastPageButton.clicked.connect(self.onLastPageBtnClicked)
        self.ui.nextPageButton.clicked.connect(self.onNextPageBtnClicked)
        self.ui.numberPerPageCB.currentTextChanged.connect(self.onNumberPerPageChanged)
        self.ui.searchButton.clicked.connect(self.onSearchBtnClicked)
        self.ui.resetSearchButton.clicked.connect(self.onResetSearchBtnClicked)
        self.ui.filterButton.toggled.connect(self.onFilterToggled)
        self.ui.searchTextEdit.returnPressed.connect(self.onSearchBtnClicked)

        if len(self.projects) == 0:
            self.ui.actionOpenProject.setDisabled(True)

    def onLastPageBtnClicked(self):
        proj = self.workingProject
        if proj is None:
            return
        proj.status["currentPage"] -= 1
        self.freshSqlView()

    def onNextPageBtnClicked(self):
        proj = self.workingProject
        if proj is None:
            return
        proj.status["currentPage"] += 1
        self.freshSqlView()

    def onNumberPerPageChanged(self, text: str):
        proj = self.workingProject
        if proj is None:
            return
        proj.status["numberPerPage"] = int(text)
        self.freshSqlView()

    def onResetSearchBtnClicked(self):
        proj: Project = self.workingProject
        ctb = proj.status.get("currentTableName", proj.projSettings["dataBase"]["table_name"])
        if ctb != proj.projSettings["dataBase"]["table_name"]:
            proj.status["currentTableName"] = proj.projSettings["dataBase"]["table_name"]
            self.freshSqlView()

    def onSearchBtnClicked(self):
        # 禁用检索按钮,防止重复检索
        if self.workingProject is None:
            return
        self.ui.searchButton.setDisabled(True)
        searchTablesName = ["TEMP_SEARCH1", "TEMP_SEARCH2"]
        proj: Project = self.workingProject
        currentTableName = proj.status.get("currentTableName", proj.projSettings['dataBase']["table_name"])
        srcTableName = proj.projSettings['dataBase']["table_name"]
        oldSearchTableName = currentTableName if currentTableName in searchTablesName else None
        if currentTableName not in searchTablesName:
            newSearchTableName = searchTablesName[0]
        else:
            searchTablesName.pop(searchTablesName.index(currentTableName))
            newSearchTableName = searchTablesName[0]

            # 新建一个用于存放检索的表
        _sql = f"CREATE TABLE {newSearchTableName} ("
        _sql += ', '.join([f'{headerData["name"]} {headerData["type"]}' for headerData in
                           proj.projSettings['dataBase']['headers']])
        _sql += ")"

        query = QSqlQuery(proj.sqlDatabase)
        query.exec(_sql)
        print(self.__class__.__name__,_sql)

        searchText = self.ui.searchTextEdit.text()
        searchMode = SearchText.getSearchMode(self.ui.searchModeBox.currentText())
        searchPattern = SearchText.getSQLLikePattern(searchText, searchMode)

        filterEnabled = self.ui.filterButton.isChecked()
        _filter = f"{self.workingProject.voiceColumnName} IS NULL AND " if filterEnabled else ""

        # 将检索结果插入新表
        _sql = f"INSERT INTO {newSearchTableName} SELECT * FROM {srcTableName} WHERE {_filter}{self.ui.columnBox.currentText()} LIKE '{searchPattern}'"
        query.exec(_sql)
        print(self.__class__.__name__,_sql)

        # 更改sqlView中的数据
        proj.status["currentTableName"] = newSearchTableName
        # 刷新sqlView
        self.freshSqlView()

        if oldSearchTableName is not None:
            _sql = f"DROP TABLE {oldSearchTableName}"
            query.exec(_sql)
            print(self.__class__.__name__,_sql)

        self.ui.searchButton.setEnabled(True)
        return

    def onOpenFileActionTriggered(self) -> None:
        _filter = ""
        for k in self.diffFileActions.keys():
            _filter += k + ";;"
        _filter = _filter[:-2]
        fileName, fi1ter = QFileDialog.getOpenFileName(filter=_filter)
        if fileName != '':
            self.diffFileActions[fi1ter](fileName)

    def onProjectsActionTriggered(self) -> None:
        self.projectsWindow.show()

    def onSaveProjectActionTriggered(self) -> None:
        if self.workingProject is not None:
            self.workingProject.save()
            print(self.__class__.__name__,f"project:{self.workingProject.projName} saved")

    def onUsageActionTriggered(self) -> None:
        QMessageBox.information(self, "信息与用法",
                                f"仓库:https://github.com/AresConnor/RenpySimpleVoiceManager\n作者:AresConnor(爱喝矿泉水)\n\n平台支持的播放格式:\n{self.ui.sqlView.supportFormat}")

    @Slot(Project)
    def onProjectReady(self, project: Project) -> None:
        # 代表了至少存在一个项目
        if not self.ui.actionOpenProject.isEnabled():
            self.ui.actionOpenProject.setEnabled(True)

        # 自动保存前一个project
        if self.workingProject is not None and self.workingProject.projName != project.projName:
            print(self.__class__.__name__,f"auto saved current project:{self.workingProject.projName}")
            self.workingProject.save()

        self.workingProject = project
        if self.workingProject is not None:
            self.ui.sqlView.setModel(project.sqlDatabaseModel)
            project.sqlDatabaseModel.dataChanged.connect(self.onSqlViewDataChanged)
            self.freshSqlView()

            self.ui.sqlView.resizeColumnsToContents()
            self.ui.sqlView.resizeRowsToContents()
            self.ui.sqlView.horizontalHeader().setStretchLastSection(True)
            self.ui.sqlView.verticalHeader().setStretchLastSection(False)

            self.ui.columnBox.addItems(
                [header["name"] for header in project.projSettings["dataBase"]["headers"] if header["type"] != "BLOB"])
            # 将检索栏的所有小部件设置为禁用
            if not self.ui.groupBox.isEnabled():
                self.ui.groupBox.setEnabled(True)

            QCoreApplication.processEvents()

    def closeWorkingProject(self) -> None:
        if self.workingProject is not None:
            self.ui.sqlView.setModel(None)
            self.workingProject.close()
            self.workingProject = None
            self.ui.columnBox.clear()
            self.ui.groupBox.setDisabled(True)

    def freshSqlView(self) -> None:
        self.workingProject: Project
        self.sqlView: QTableView
        proj = self.workingProject
        if not proj.isOpen():
            proj.open()
        currentTableName = proj.status.get("currentTableName", proj.projSettings["dataBase"]["table_name"])

        filterEnabled = self.ui.filterButton.isChecked()
        _filter = f"WHERE {self.workingProject.voiceColumnName} IS NULL " if filterEnabled else ""
        numPerPage = int(self.ui.numberPerPageCB.currentText())
        page = proj.status.get("currentPage", 0)
        maxIndex = proj.getDBTotalNum(_filter)

        maxPage = maxIndex // numPerPage if maxIndex % numPerPage == 0 else maxIndex // numPerPage + 1
        if page < 1:
            page = 1
            proj.status["currentPage"] = 1
        elif page == 1:
            self.ui.lastPageButton.setDisabled(True)
        elif 1 < page < maxPage:
            self.ui.lastPageButton.setDisabled(False)
            self.ui.nextPageButton.setDisabled(False)
        elif page == maxPage:
            self.ui.nextPageButton.setDisabled(True)
        elif page > maxPage:
            page = maxPage
            proj.status["currentPage"] = maxPage

        self.ui.currentPageLabel.setText(f"{page}/{maxPage}")
        beginIndex = page * numPerPage - numPerPage
        query = QSqlQuery(
            f"select * from {currentTableName} {_filter}limit {beginIndex}, {self.ui.numberPerPageCB.currentText()}")
        self.ui.sqlView.model().setQuery(query)
        print(self.__class__.__name__,query.lastQuery())

    def onSqlViewDataChanged(self, topLeft, bottomRight, roles=...) -> None:
        self.freshSqlView()

    def onFilterToggled(self, check: bool) -> None:
        self.freshSqlView()

    def onSaveFile(self):
        pass

    def initFileActions(self) -> None:

        self.diffFileActions = {
            "制表文件 (*.tab)": self.createNewProject,
            "数据库 (*.db)": lambda _, fileName: print(self.__class__.__name__,"暂未实现")
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
                        self.projects.pop(projName).remove()
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
            i = 1
            for _data in data:
                _data = translateCharacter(_data, self.charaDefine)
                _data.insert(0, i)
                _data.extend([None, ""])
                projObj.dataBaseInsertData(_data)

                progressDialog.setValue(i)
                QCoreApplication.processEvents()
                if progressDialog.wasCanceled():
                    projObj.remove()
                    self.projects.pop(projName)
                    return None
                i += 1
            progressDialog.setValue(len(data))

            # 保存Projects.json
            with open("Projects/Projects.json", "w", encoding='utf-8') as f:
                json.dump({projObj.projName: projObj.projSettings for projObj in self.projects.values()}, f,
                          ensure_ascii=False, sort_keys=True, indent=4)

            self.projectReadySignal.emit(projObj)

            return None
        else:
            return None

    def onOpenProjectActionTriggered(self) -> None:
        projName, received = QInputDialog.getItem(self, "打开项目...", "请选择项目", self.projects.keys(), 0, False,
                                                  Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        if received:
            self.projectReadySignal.emit(self.projects[projName])

    def initProjectsWindow(self):
        self.projectsWindow = ProjectDialog(parent=self)

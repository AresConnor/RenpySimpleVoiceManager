# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

from RenpySimpleVoiceManager.VoiceManager.ProjectView import ProjectView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(873, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchTextEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchTextEdit.sizePolicy().hasHeightForWidth())
        self.searchTextEdit.setSizePolicy(sizePolicy)
        self.searchTextEdit.setObjectName("searchTextEdit")
        self.horizontalLayout.addWidget(self.searchTextEdit)
        self.columnBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.columnBox.sizePolicy().hasHeightForWidth())
        self.columnBox.setSizePolicy(sizePolicy)
        self.columnBox.setObjectName("columnBox")
        self.horizontalLayout.addWidget(self.columnBox)
        self.searchModeBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchModeBox.sizePolicy().hasHeightForWidth())
        self.searchModeBox.setSizePolicy(sizePolicy)
        self.searchModeBox.setObjectName("searchTypeBox")
        self.horizontalLayout.addWidget(self.searchModeBox)
        self.searchButton = QtWidgets.QPushButton(self.groupBox)
        self.searchButton.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.searchButton)
        self.resetSearchButton = QtWidgets.QPushButton(self.groupBox)
        self.resetSearchButton.setObjectName("cancelSearchButton")
        self.horizontalLayout.addWidget(self.resetSearchButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.numberPerPageCB = QtWidgets.QComboBox(self.groupBox_2)
        self.numberPerPageCB.setObjectName("numberPerPageCB")
        self.numberPerPageCB.addItem("")
        self.numberPerPageCB.addItem("")
        self.numberPerPageCB.addItem("")
        self.horizontalLayout_4.addWidget(self.numberPerPageCB)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.filterButton = QtWidgets.QRadioButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterButton.sizePolicy().hasHeightForWidth())
        self.filterButton.setSizePolicy(sizePolicy)
        self.filterButton.setObjectName("filterButton")
        self.verticalLayout_3.addWidget(self.filterButton)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sqlView = ProjectView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sqlView.sizePolicy().hasHeightForWidth())
        self.sqlView.setSizePolicy(sizePolicy)
        self.sqlView.setAcceptDrops(True)
        self.sqlView.setDragEnabled(True)
        #self.sqlView.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.sqlView.setObjectName("sqlView")
        self.verticalLayout.addWidget(self.sqlView)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.lastPageButton = QtWidgets.QPushButton(self.centralwidget)
        self.lastPageButton.setObjectName("lastPageButton")
        self.horizontalLayout_3.addWidget(self.lastPageButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.currentPageLabel = QtWidgets.QLabel(self.centralwidget)
        self.currentPageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.currentPageLabel.setObjectName("currentPageLabel")
        self.horizontalLayout_3.addWidget(self.currentPageLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.nextPageButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextPageButton.setObjectName("nextPageButton")
        self.horizontalLayout_3.addWidget(self.nextPageButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 873, 22))
        self.menuBar.setObjectName("menuBar")
        self.fileMenu = QtWidgets.QMenu(self.menuBar)
        self.fileMenu.setObjectName("fileMenu")
        self.operateMenu = QtWidgets.QMenu(self.menuBar)
        self.operateMenu.setObjectName("operateMenu")
        self.helpMenu = QtWidgets.QMenu(self.menuBar)
        self.helpMenu.setObjectName("helpMenu")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionundo = QtGui.QAction(MainWindow)
        self.actionundo.setObjectName("actionundo")
        self.actionredo = QtGui.QAction(MainWindow)
        self.actionredo.setObjectName("actionredo")
        self.actionusage = QtGui.QAction(MainWindow)
        self.actionusage.setObjectName("actionusage")
        self.actionOpenProject = QtGui.QAction(MainWindow)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionSaveProject = QtGui.QAction(MainWindow)
        self.actionSaveProject.setObjectName("actionSaveProject")
        self.actionProjects = QtGui.QAction(MainWindow)
        self.actionProjects.setObjectName("actionProjects")
        self.fileMenu.addAction(self.actionOpen)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actionOpenProject)
        self.fileMenu.addAction(self.actionSaveProject)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actionProjects)
        self.operateMenu.addAction(self.actionundo)
        self.operateMenu.addAction(self.actionredo)
        self.helpMenu.addAction(self.actionusage)
        self.menuBar.addAction(self.fileMenu.menuAction())
        self.menuBar.addAction(self.operateMenu.menuAction())
        self.menuBar.addAction(self.helpMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RenPy 自动语音管理工具"))
        self.groupBox.setTitle(_translate("MainWindow", "检索栏"))
        self.searchButton.setText(_translate("MainWindow", "检索"))
        self.resetSearchButton.setText(_translate("MainWindow", "取消检索"))
        self.groupBox_2.setTitle(_translate("MainWindow", "控制栏"))
        self.label.setText(_translate("MainWindow", "每页显示数"))
        self.numberPerPageCB.setItemText(0, _translate("MainWindow", "100"))
        self.numberPerPageCB.setItemText(1, _translate("MainWindow", "200"))
        self.numberPerPageCB.setItemText(2, _translate("MainWindow", "500"))
        self.filterButton.setText(_translate("MainWindow", "只显示未添加音频的条目"))
        self.lastPageButton.setText(_translate("MainWindow", "上一页"))
        self.currentPageLabel.setText(_translate("MainWindow", "NaN/NaN 页"))
        self.nextPageButton.setText(_translate("MainWindow", "下一页"))
        self.fileMenu.setTitle(_translate("MainWindow", "文件"))
        self.operateMenu.setTitle(_translate("MainWindow", "操作"))
        self.helpMenu.setTitle(_translate("MainWindow", "帮助"))
        self.actionOpen.setText(_translate("MainWindow", "打开"))
        self.actionundo.setText(_translate("MainWindow", "撤销(未实现)"))
        self.actionredo.setText(_translate("MainWindow", "重做(未实现)"))
        self.actionusage.setText(_translate("MainWindow", "用法与信息"))
        self.actionOpenProject.setText(_translate("MainWindow", "打开项目"))
        self.actionSaveProject.setText(_translate("MainWindow", "保存项目"))
        self.actionProjects.setText(_translate("MainWindow", "项目列表"))
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(650, 550))
        MainWindow.setMaximumSize(QtCore.QSize(650, 550))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_frame_2 = QtWidgets.QFrame(self.centralWidget)
        self.top_frame_2.setMinimumSize(QtCore.QSize(0, 30))
        self.top_frame_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.top_frame_2.setAutoFillBackground(True)
        self.top_frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.top_frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.top_frame_2.setLineWidth(0)
        self.top_frame_2.setObjectName("top_frame_2")
        self.ltitle_label = QtWidgets.QLabel(self.top_frame_2)
        self.ltitle_label.setGeometry(QtCore.QRect(12, 12, 602, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ltitle_label.sizePolicy().hasHeightForWidth())
        self.ltitle_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.ltitle_label.setFont(font)
        self.ltitle_label.setAutoFillBackground(False)
        self.ltitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ltitle_label.setObjectName("ltitle_label")
        self.verticalLayout.addWidget(self.top_frame_2)
        self.frame_3 = QtWidgets.QFrame(self.centralWidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.name_frame = QtWidgets.QFrame(self.frame_3)
        self.name_frame.setMaximumSize(QtCore.QSize(130, 16777215))
        self.name_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.name_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.name_frame.setObjectName("name_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.name_frame)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.name_label = QtWidgets.QLabel(self.name_frame)
        self.name_label.setMaximumSize(QtCore.QSize(16777215, 12))
        self.name_label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.name_label.setWordWrap(False)
        self.name_label.setObjectName("name_label")
        self.verticalLayout_3.addWidget(self.name_label)
        self.name_listWidget = QtWidgets.QListWidget(self.name_frame)
        self.name_listWidget.setMaximumSize(QtCore.QSize(100, 400))
        self.name_listWidget.setObjectName("name_listWidget")
        self.verticalLayout_3.addWidget(self.name_listWidget)
        self.horizontalLayout_2.addWidget(self.name_frame)
        self.frame_2 = QtWidgets.QFrame(self.frame_3)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 12)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.top_frame = QtWidgets.QFrame(self.frame_2)
        self.top_frame.setMaximumSize(QtCore.QSize(16777215, 160))
        self.top_frame.setAutoFillBackground(False)
        self.top_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.top_frame.setObjectName("top_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.top_frame)
        self.horizontalLayout.setContentsMargins(11, 0, 11, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.money_frame = QtWidgets.QFrame(self.top_frame)
        self.money_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.money_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.money_frame.setObjectName("money_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.money_frame)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.now_label = QtWidgets.QLabel(self.money_frame)
        self.now_label.setObjectName("now_label")
        self.gridLayout.addWidget(self.now_label, 1, 0, 1, 1)
        self.yearly_lineEdit = QtWidgets.QLineEdit(self.money_frame)
        self.yearly_lineEdit.setEnabled(False)
        self.yearly_lineEdit.setObjectName("yearly_lineEdit")
        self.gridLayout.addWidget(self.yearly_lineEdit, 0, 1, 1, 1)
        self.yearly_label = QtWidgets.QLabel(self.money_frame)
        self.yearly_label.setObjectName("yearly_label")
        self.gridLayout.addWidget(self.yearly_label, 0, 0, 1, 1)
        self.submit_lineEdit = QtWidgets.QLineEdit(self.money_frame)
        self.submit_lineEdit.setObjectName("submit_lineEdit")
        self.gridLayout.addWidget(self.submit_lineEdit, 1, 1, 1, 1)
        self.remain_lineEdit = QtWidgets.QLineEdit(self.money_frame)
        self.remain_lineEdit.setEnabled(False)
        self.remain_lineEdit.setObjectName("remain_lineEdit")
        self.gridLayout.addWidget(self.remain_lineEdit, 2, 1, 1, 1)
        self.remain_label = QtWidgets.QLabel(self.money_frame)
        self.remain_label.setObjectName("remain_label")
        self.gridLayout.addWidget(self.remain_label, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.money_frame)
        self.buttom_frame = QtWidgets.QFrame(self.top_frame)
        self.buttom_frame.setMaximumSize(QtCore.QSize(140, 16777215))
        self.buttom_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.buttom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttom_frame.setObjectName("buttom_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.buttom_frame)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.submit_pushButton = QtWidgets.QPushButton(self.buttom_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit_pushButton.sizePolicy().hasHeightForWidth())
        self.submit_pushButton.setSizePolicy(sizePolicy)
        self.submit_pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.submit_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.submit_pushButton.setFont(font)
        self.submit_pushButton.setIconSize(QtCore.QSize(16, 16))
        self.submit_pushButton.setCheckable(False)
        self.submit_pushButton.setObjectName("submit_pushButton")
        self.verticalLayout_2.addWidget(self.submit_pushButton)
        self.cancel_pushButton = QtWidgets.QPushButton(self.buttom_frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cancel_pushButton.setFont(font)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.verticalLayout_2.addWidget(self.cancel_pushButton)
        self.horizontalLayout.addWidget(self.buttom_frame)
        self.verticalLayout_5.addWidget(self.top_frame)
        self.middle_frame = QtWidgets.QFrame(self.frame_2)
        self.middle_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.middle_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.middle_frame.setLineWidth(0)
        self.middle_frame.setObjectName("middle_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.middle_frame)
        self.horizontalLayout_3.setContentsMargins(11, 0, 11, 0)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.init_pushButton = QtWidgets.QPushButton(self.middle_frame)
        self.init_pushButton.setEnabled(False)
        self.init_pushButton.setObjectName("init_pushButton")
        self.horizontalLayout_3.addWidget(self.init_pushButton)
        self.addstaff_pushButton = QtWidgets.QPushButton(self.middle_frame)
        self.addstaff_pushButton.setObjectName("addstaff_pushButton")
        self.horizontalLayout_3.addWidget(self.addstaff_pushButton)
        self.pushButton = QtWidgets.QPushButton(self.middle_frame)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout_5.addWidget(self.middle_frame)
        self.bottom_frame = QtWidgets.QFrame(self.frame_2)
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom_frame.setObjectName("bottom_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.bottom_frame)
        self.verticalLayout_4.setContentsMargins(11, 0, 11, 0)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.history_label = QtWidgets.QLabel(self.bottom_frame)
        self.history_label.setObjectName("history_label")
        self.verticalLayout_4.addWidget(self.history_label)
        self.history_textBrowser = QtWidgets.QTextBrowser(self.bottom_frame)
        self.history_textBrowser.setObjectName("history_textBrowser")
        self.verticalLayout_4.addWidget(self.history_textBrowser)
        self.verticalLayout_5.addWidget(self.bottom_frame)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame_3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setEnabled(False)
        self.mainToolBar.setMaximumSize(QtCore.QSize(16777215, 0))
        self.mainToolBar.setWindowTitle("")
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setEnabled(False)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.ltitle_label.setBuddy(self.ltitle_label)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AccountBook"))
        self.ltitle_label.setText(_translate("MainWindow", "______交通费报销登记系统"))
        self.name_label.setText(_translate("MainWindow", "请选择员工"))
        self.name_listWidget.setSortingEnabled(True)
        self.now_label.setText(_translate("MainWindow", "本次报销(元)："))
        self.yearly_label.setText(_translate("MainWindow", "年度总额(元)："))
        self.remain_label.setText(_translate("MainWindow", "年度剩余(元)："))
        self.submit_pushButton.setText(_translate("MainWindow", "提交"))
        self.cancel_pushButton.setText(_translate("MainWindow", "撤销"))
        self.init_pushButton.setText(_translate("MainWindow", "初始化"))
        self.addstaff_pushButton.setText(_translate("MainWindow", "新员工导入"))
        self.pushButton.setText(_translate("MainWindow", "输出记录"))
        self.history_label.setText(_translate("MainWindow", "历史记录："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


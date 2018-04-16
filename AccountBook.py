#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mainwindow import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QInputDialog, QLineEdit
from PyQt5.QtCore import QDir


class AccountBook(QMainWindow):
    def __init__(self):
        # QtWidgets.QDialog.__init__(self)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.apply_pushButton.clicked.connect(self.apply_PushButtonClicked)
        self.ui.cancel_pushButton.clicked.connect(
            self.cancel_PushButtonClicked)
        self.show()

    def apply_PushButtonClicked(self):
        # box = QMessageBox()
        # box.information(self, 'Message', '你已提交成功')
        box = QInputDialog()
        text, ok = box.getText(
            self,
            'add person',
            'Input Name:', QLineEdit.Normal, QDir.home().dirName()
        )
        if ok and text != '':
            self.ui.name_listWidget.addItem(text)

    def cancel_PushButtonClicked(self):
        msgBox = QMessageBox(QMessageBox.Warning, "Warning!", '确定要撤销本次操作吗？',
                             QMessageBox.NoButton, self)
        msgBox.addButton("Yes, cancel now!", QMessageBox.AcceptRole)
        msgBox.addButton("No", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            pass
        else:
            pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = AccountBook()
    sys.exit(app.exec_())

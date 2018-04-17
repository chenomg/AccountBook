#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mainwindow import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QInputDialog, QLineEdit
from PyQt5.QtCore import QDir
import sqlite3
import xlrd
import os


class AccountBook(QMainWindow):
    def __init__(self):
        # QtWidgets.QDialog.__init__(self)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.apply_pushButton.clicked.connect(self.apply_PushButtonClicked)
        self.ui.cancel_pushButton.clicked.connect(
            self.cancel_PushButtonClicked)

        # 检测是否存在db.sqlit不存在的话则根据表格创建数据库
        sqlite_exist = self.sqlite_exist()
        if not sqlite_exist:
            self.ui.init_pushButton.setEnabled(True)
            self.ui.init_pushButton.clicked.connect(self.init)

        # name_listWidget显示员工清单
        if sqlite_exist:
            names = self.get_Name_List()
            for name in names:
                self.ui.name_listWidget.addItem(name)


        self.show()

    def apply_PushButtonClicked(self):
        # box = QMessageBox()
        # box.information(self, 'Message', '你已提交成功')
        box = QInputDialog()
        text, ok = box.getText(self, 'add person', 'Input Name:',
                               QLineEdit.Normal,
                               QDir.home().dirName())
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

    def init(self):
        """
        根据表格内容创建数据库
        """
        filename = 'data.xls'
        data = xlrd.open_workbook(filename)
        conn = sqlite3.connect('db.sqlite')
        conn.execute(u'''CREATE TABLE DATASHEET(
        序号 INT PRIMARY KEY NOT NULL,
        姓名 CHAR(10) NOT NULL,
        '1月' INT,
        '2月' INT,
        '3月' INT,
        '4月' INT,
        '5月' INT,
        '6月' INT,
        '7月' INT,
        '8月' INT,
        '9月' INT,
        '10月' INT,
        '11月' INT,
        '12月' INT,
        每月额度 INT NOT NULL,
        有效月数 INT NOT NULL,
        年额度 INT NOT NULL,
        已支取 INT NOT NULL,
        剩余额度 INT NOT NULL);''')
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows - 1):
            insertDatas = table.row_values(i + 1)
            conn.execute('''INSERT INTO DATASHEET(
            序号,姓名,"1月",'2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',每月额度,有效月数,年额度,已支取,剩余额度
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (insertDatas))
        conn.commit()
        conn.close()
        self.ui.init_pushButton.setEnabled(False)

    def get_Name_List(self):
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT 姓名 FROM DATASHEET')
        names = cursor.fetchall()
        return [name[0] for name in names]

    def sqlite_exist(self):
        path = os.getcwd()
        file_list = os.listdir(path)
        for f in file_list:
            if not os.path.isdir(f):
                if f == 'db.sqlite':
                    return True
        else:
            return False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = AccountBook()
    sys.exit(app.exec_())

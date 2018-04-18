#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mainwindow import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QInputDialog, QLineEdit
from PyQt5.QtCore import QDir
import sqlite3
import xlrd
import os
import datetime


class AccountBook(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置初始数值
        self.name_selected = ''
        self.total_selected = 0
        self.remain_selected = 0
        self.submit_value = 0

        # 启动UI
        # super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.yearly_lineEdit.setText(str(self.total_selected))
        self.ui.remain_lineEdit.setText(str(self.remain_selected))
        self.ui.submit_lineEdit.setText(str(self.submit_value))

        # 检测是否存在db.sqlit不存在的话则按下初始化按钮后根据表格创建数据库
        self.sqlite_exist()
        if not self.sqlite_exist():
            self.ui.init_pushButton.setEnabled(True)
            self.ui.init_pushButton.clicked.connect(self.init)
        else:
            # 姓名栏显示员工姓名
            self.show_Name_listWidge()

        # 设置事件动作
        self.ui.submit_pushButton.clicked.connect(
            self.submit_PushButtonClicked)
        self.ui.cancel_pushButton.clicked.connect(
            self.cancel_PushButtonClicked)
        # 如果有员工被选中则在右边显示相关信息
        self.ui.name_listWidget.itemClicked.connect(self.show_Selected_Info)

        self.show()

    def get_month(self):
        """
        renturn now month just like 4 (means:APRIL)
        """
        now = datetime.datetime.now()
        return now.month

    def show_Selected_Info(self, item):
        # 如果有员工被选中则在右边显示相关信息
        self.name_selected = self.ui.name_listWidget.selectedItems()[0].text()
        print(str(type(self.name_selected)) + ':' + self.name_selected)
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT TOTAL, REMAIN FROM DATASHEET WHERE NAME=?",
                       (self.name_selected, ))
        infos = cursor.fetchall()
        if infos:
            for info in infos:
                self.total_selected = info[0]
                self.remain_selected = info[1]
                self.ui.yearly_lineEdit.setText(str(self.total_selected))
                self.ui.remain_lineEdit.setText(str(self.remain_selected))
        else:
            self.ui.yearly_lineEdit.setText('0')
            self.ui.remain_lineEdit.setText('0')
        cursor.close()

    def show_Name_listWidge(self):
        # 检测是否存在db.sqlit不存在的话则根据表格创建数据库
        sqlite_exist = self.sqlite_exist()
        # name_listWidget显示员工清单
        if sqlite_exist:
            names = self.get_Name_List()
            for name in names:
                self.ui.name_listWidget.addItem(name)

    def submit_PushButtonClicked(self):
        if self.name_selected:
            submit_value = self.ui.submit_lineEdit.text()
            month_id = self.get_month()
            months = [
                'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP',
                'OCT', 'NOV', 'DEC'
            ]
            month = months[month_id - 1]
            print(month)
            # 更新数据库数据
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ?, EXTRACTED, REMAIN FROM DATASHEET WHERE NAME = ?",
                (month, self.name_selected, ))
            datas = cursor.fetchall()
            print(datas)
            for data in datas:
                month_value = data[0]
                extracted_value = data[1]
                remain_value = data[2]
            cursor.execute(
                "UPDATE DATASHEET SET ? = ?, EXTRACTED = ?, REMAIN = ?",
                (month, month_value, int(extracted_value) + int(submit_value),
                 int(remain_value) - int(submit_value),))
            cursor.commit()
            cursor.close()
            # print(submit_value)
            box = QMessageBox()
            box.information(self, 'Message', '你已提交成功')
        else:
            box = QMessageBox()
            box.information(self, 'Message', '请选择员工进行操！')

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
        ID INT PRIMARY KEY NOT NULL,
        NAME CHAR(10) NOT NULL,
        JAN INT,
        FEB INT,
        MAR INT,
        APR INT,
        MAY INT,
        JUN INT,
        JUL INT,
        AUG INT,
        SEP INT,
        OCT INT,
        NOV INT,
        DEC INT,
        MONTHLY INT NOT NULL,
        MONTHS INT NOT NULL,
        TOTAL INT NOT NULL,
        EXTRACTED INT NOT NULL,
        REMAIN INT NOT NULL);''')
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows - 1):
            insertDatas = table.row_values(i + 1)
            conn.execute('''INSERT INTO DATASHEET(
            ID,NAME,JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC,MONTHLY,MONTHS,TOTAL,EXTRACTED,REMAIN
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (insertDatas))
        conn.commit()
        conn.close()
        self.ui.init_pushButton.setEnabled(False)
        self.show_Name_listWidge()

    def get_Name_List(self):
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT NAME FROM DATASHEET')
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

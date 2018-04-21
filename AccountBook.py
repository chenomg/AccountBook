#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
import sqlite3
import xlrd
import os
import datetime
import re
from platform import platform


class AccountBook(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置初始数值
        self.name_selected = ''
        self.total_selected = 0
        self.remain_selected = 0
        self.submit_value = 0
        # 设置撤销按钮参数
        self.cancel_count = 0
        self.cancel_name = ''
        self.cancel_value = 0
        self.cancel_month = ''
        # 检测是否为Windows平台
        self.Platform = platform()

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

    def update_info(self):
        # 更新用户信息，包括年度总额，剩余总额和历史记录
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
        # 更新历史记录栏信息
        cursor.execute(
            "SELECT NAME, UPDATETIME, SUBMIT, EXTRACTED_UPDATE, REMAIN_UPDATE FROM HISTORY WHERE NAME=?",
            (self.name_selected, ))
        infos = cursor.fetchall()
        print(infos)
        if infos:
            history_one_text = []
            history_text_list = []
            for info in infos:
                print(info)
                string = str(info[0]) + ":于" + str(info[1]) + ' 提交:' + str(
                    info[2]) + ' 共支取:' + str(info[3]) + ' 剩余:' + str(info[4])
                history_text_list.append(string)
                print(history_text_list)
            # for t in range(len(history_text_list)-1,0,-1):
            out = '\n'.join(history_text_list)
            self.ui.history_textBrowser.setText(out)
        else:
            self.ui.history_textBrowser.setText('')
        cursor.close()
        conn.close()

    def update_db(self, name, month, value):
        # 更新数据库数据
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        # 获取现在数据库内数据
        sql = "SELECT " + month + \
            ", EXTRACTED, REMAIN FROM DATASHEET WHERE NAME = '" + name + "'"
        cursor.execute(sql)
        datas = cursor.fetchall()
        for data in datas:
            month_value = data[0]
            if not month_value:
                month_value = 0
            extracted_value = data[1]
            remain_value = data[2]
            extracted_value_update = extracted_value + value
            remain_value_update = remain_value - value
        # 更新数据库内数据
        sql2 = "UPDATE DATASHEET SET " + month + " = " + str(
            month_value + value) + ", EXTRACTED = " + str(
                extracted_value_update) + ", REMAIN = " + str(
                    remain_value_update) + " WHERE NAME = '" + str(name) + "'"
        cursor.execute(sql2)
        conn.commit()
        # 更新历史记录
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        c = cursor.execute("SELECT * FROM HISTORY")
        history_rows = len(c.fetchall())
        Id = int(history_rows) + 1
        updatetime = datetime.datetime.now()
        updatetime_str = updatetime.strftime("%Y-%m-%d %H:%M:%S")
        sql3 = "INSERT INTO HISTORY(ID, UPDATETIME, NAME, SUBMIT, EXTRACTED_UPDATE, REMAIN_UPDATE)\
            VALUES({ID}, '{UPDATETIME}', '{NAME}', '{SUBMIT}', '{EXTRACTED_UPDATE}', '{REMAIN_UPDATE}');".format(
            ID=Id,
            UPDATETIME=updatetime_str,
            NAME=name,
            SUBMIT=value,
            EXTRACTED_UPDATE=extracted_value_update,
            REMAIN_UPDATE=remain_value_update)
        cursor.execute(sql3)
        conn.commit()
        cursor.close()
        conn.close()

    def show_Selected_Info(self, item):
        # 如果有员工被选中则在右边显示相关信息
        self.name_selected = self.ui.name_listWidget.selectedItems()[0].text()
        print(str(type(self.name_selected)) + ':' + self.name_selected)
        self.update_info()

    def show_Name_listWidge(self):
        # 检测是否存在db.sqlit不存在的话则根据表格创建数据库
        # name_listWidget显示员工清单
        if self.sqlite_exist():
            names = self.get_Name_List()
            for name in names:
                self.ui.name_listWidget.addItem(name)
        else:
            print("There's no db.sqlite file exists!")

    def submit_PushButtonClicked(self):
        if self.name_selected:
            submit_value = int(self.ui.submit_lineEdit.text())
            if submit_value:
                month_id = self.get_month()
                months = [
                    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG',
                    'SEP', 'OCT', 'NOV', 'DEC'
                ]
                month = months[month_id - 1]
                # 更新数据库数据
                self.update_db(
                    name=self.name_selected, month=month, value=submit_value)
                self.cancel_name = self.name_selected
                self.cancel_value = submit_value
                self.cancel_month = month
                self.cancel_count = 1
                box = QMessageBox()
                box.information(self, 'Message', '提交成功')
                self.update_info()
                # 更新数据后将提交输入栏置零，防止误操作
                self.ui.submit_lineEdit.setText('0')
            else:
                box = QMessageBox()
                box.information(self, 'Message', '请输入数据')
        else:
            box = QMessageBox()
            box.information(self, 'Message', '请选择员工进行操作！')

    def cancel_PushButtonClicked(self):
        msgBox = QMessageBox(
            QMessageBox.Warning, "Warning!",
            '确定要撤销本次操作吗？\n' + self.cancel_name + ': ' + str(self.cancel_value),
            QMessageBox.NoButton, self)
        msgBox.addButton("Yes!", QMessageBox.AcceptRole)
        msgBox.addButton("No", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            if self.cancel_count:
                self.update_db(
                    name=self.cancel_name,
                    month=self.cancel_month,
                    value=-self.cancel_value)
                self.cancel_count = 0
                QMessageBox().information(self, 'Message', '撤销成功')
                self.update_info()
                # 更新数据后将提交输入栏置零，防止误操作
                self.ui.submit_lineEdit.setText('0')
            else:
                QMessageBox().information(self, 'Message', '当前无法撤销')
        else:
            pass

    def init(self):
        """
        根据表格内容创建数据库
        """
        # 创建员工信息表
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
        # 创建操作记录数据库记录表
        conn = sqlite3.connect('db.sqlite')
        conn.execute(u'''CREATE TABLE HISTORY(
            ID INT PRIMARY KEY NOT NULL,
            UPDATETIME CHAR(30),
            NAME CHAR(10),
            SUBMIT INT,
            EXTRACTED_UPDATE INT,
            REMAIN_UPDATE INT);''')
        conn.commit()
        conn.close()
        # 初始化按钮不可用
        self.ui.init_pushButton.setEnabled(False)
        self.show_Name_listWidge()
        if re.findall(r'^windows.*', self.Platform, re.I):
            import win32con
            import win32api
            # 隐藏数据库文件
            win32api.SetFileAttributes('db.sqlite',
                                       win32con.FILE_ATTRIBUTE_HIDDEN)
        else:
            pass

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

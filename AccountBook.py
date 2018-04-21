#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: AccountBook.py
#          Desc: use to record the account
#        Author: Jase Chen
#         Email: xxmm@live.cn
#      HomePage: http://jase.im/
#       Version: 0.0.1
#    LastChange: 2018-04-21 20:56:09
#       History:
# =============================================================================
'''
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
        # 设置提取时金额不能过大，默认为最大只能提取到下个月为止，若过大会提醒
        self.over_months = 1
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
        if not self.sqlite_exist():
            self.ui.init_pushButton.setEnabled(True)
            self.ui.init_pushButton.clicked.connect(self.init)
        else:
            # 姓名栏显示员工姓名
            self.show_Name_listWidge()
            # 设置初始历史记录显示
            self.update_info()

        # 设置事件动作
        self.ui.submit_pushButton.clicked.connect(
            self.submit_PushButtonClicked)
        self.ui.cancel_pushButton.clicked.connect(
            self.cancel_PushButtonClicked)
        # 如果有员工被选中则在右边显示相关信息
        self.ui.name_listWidget.itemClicked.connect(self.show_Selected_Info)
        # 提交栏内输入完后按回车键直接提交
        self.ui.submit_lineEdit.returnPressed.connect(
            self.submit_PushButtonClicked)
        # 增加新员工按钮
        self.ui.addstaff_pushButton.clicked.connect(
            self.addStaff_PushButtonClicked)

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
        if self.name_selected:
            cursor.execute(
                "SELECT NAME, UPDATETIME, SUBMIT, EXTRACTED_UPDATE, REMAIN_UPDATE FROM HISTORY WHERE NAME=?",
                (self.name_selected, ))
        else:
            cursor.execute(
                "SELECT NAME, UPDATETIME, SUBMIT, EXTRACTED_UPDATE, REMAIN_UPDATE FROM HISTORY"
            )
        infos = cursor.fetchall()
        if infos:
            history_text_list = []
            for info in infos:
                string = str(info[0]) + ":于" + str(info[1]) + ' 提交:' + str(
                    info[2]) + ' 共支取:' + str(info[3]) + ' 剩余:' + str(info[4])
                history_text_list.append(string)
            history_text_list_reversed = history_text_list[::-1]
            print(history_text_list_reversed)
            out = '\n'.join(history_text_list_reversed)
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
        print('history_rows: {}'.format(history_rows))
        if value > 0:
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
        else:
            sql3 = "DELETE FROM HISTORY WHERE ID = {}".format(history_rows)
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
            self.ui.name_listWidget.clear()
            for name in names:
                self.ui.name_listWidget.addItem(name)
        else:
            print("There's no db.sqlite file exists!")

    def submit_Value_Check(self, submit_value, month_now, monthly, remain):
        # 用来检查当前输入值是否过大（最大只能超前一个月领取）
        remain_update_minimum = monthly * (12 - month_now - self.over_months)
        if remain - submit_value >= remain_update_minimum:
            return True
        else:
            return False

    def submit_PushButtonClicked(self):
        # 提交按钮
        if self.name_selected:
            submit_str = self.ui.submit_lineEdit.text()
            if re.findall(r'^\d+\.?$', submit_str):
                submit_value = int(self.ui.submit_lineEdit.text())
                if submit_value:
                    month_id = self.get_month()
                    months = [
                        'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG',
                        'SEP', 'OCT', 'NOV', 'DEC'
                    ]
                    month = months[month_id - 1]
                    # 先判断数据提交后资金提取值是否过大，只能按照最大超前一个月提取交通费，不然给与提醒后再添加
                    conn = sqlite3.connect('db.sqlite')
                    cursor = conn.cursor()
                    sql = "SELECT MONTHLY, REMAIN FROM DATASHEET WHERE NAME = '{name}'".format(
                        name=self.name_selected)
                    cursor.execute(sql)
                    infos = cursor.fetchall()
                    if infos:
                        for info in infos:
                            monthly = info[0]
                            remain = info[1]
                    else:
                        pass
                    if self.submit_Value_Check(submit_value, month_id, monthly,
                                               remain):
                        # 更新数据库数据
                        self.update_db(
                            name=self.name_selected,
                            month=month,
                            value=submit_value)
                        self.cancel_name = self.name_selected
                        self.cancel_value = submit_value
                        self.cancel_month = month
                        self.cancel_count = 1
                        box = QMessageBox()
                        box.information(self, 'Message', '提交成功')
                        self.update_info()
                    else:
                        msgBox = QMessageBox(QMessageBox.Warning, "Warning!",
                                             '提交数据过大，请核对！\n确认提交？',
                                             QMessageBox.NoButton, self)
                        msgBox.addButton("Yes!", QMessageBox.AcceptRole)
                        msgBox.addButton("No", QMessageBox.RejectRole)
                        if msgBox.exec_() == QMessageBox.AcceptRole:
                            # 更新数据库数据
                            self.update_db(
                                name=self.name_selected,
                                month=month,
                                value=submit_value)
                            self.cancel_name = self.name_selected
                            self.cancel_value = submit_value
                            self.cancel_month = month
                            self.cancel_count = 1
                            box = QMessageBox()
                            box.information(self, 'Message', '提交成功')
                            self.update_info()
                        else:
                            box = QMessageBox()
                            box.information(self, 'Message', '已取消~')
                    # 更新数据后将提交输入栏置零，防止误操作
                    self.ui.submit_lineEdit.setText('0')
                else:
                    box = QMessageBox()
                    box.information(self, 'Message', '请输入数据')
            else:
                box = QMessageBox()
                box.information(self, 'Message', '请检查数据是否正确!\n请输入整数。。。')
        else:
            box = QMessageBox()
            box.information(self, 'Message', '请选择员工进行操作！')

    def cancel_PushButtonClicked(self):
        if self.cancel_count:
            msgBox = QMessageBox(QMessageBox.Warning, "Warning!",
                                 '确定要撤销本次操作吗？\n' + self.cancel_name + ': ' +
                                 str(self.cancel_value), QMessageBox.NoButton,
                                 self)
            msgBox.addButton("Yes!", QMessageBox.AcceptRole)
            msgBox.addButton("No", QMessageBox.RejectRole)
            if msgBox.exec_() == QMessageBox.AcceptRole:
                self.update_db(
                    name=self.cancel_name,
                    month=self.cancel_month,
                    value=-self.cancel_value)
                self.cancel_count = 0
                QMessageBox().information(self, 'Message', '撤销成功')
                self.update_info()
                # 更新数据后将提交输入栏置零，防止误操作
                self.ui.submit_lineEdit.setText('0')
                self.update_info()
            else:
                pass
        else:
            QMessageBox().information(self, 'Message', '当前无法撤销')

    def addStaff_PushButtonClicked(self):
        """
        根据表格内容把新员工信息更新在数据库
        """
        # 增加新员工信息表
        if self.sqlite_exist():
            filename = 'data.xls'
            data = xlrd.open_workbook(filename)
            conn = sqlite3.connect('db.sqlite')
            table = data.sheets()[0]
            nrows = table.nrows
            count = 0
            for i in range(nrows - 1):
                insertDatas = table.row_values(i + 1)
                if insertDatas[1] not in self.get_Name_List():
                    conn.execute('''INSERT INTO DATASHEET(
                    ID,NAME,JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC,MONTHLY,MONTHS,TOTAL,EXTRACTED,REMAIN
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                 (insertDatas))
                    count += 1
                else:
                    pass
            box = QMessageBox()
            if count:
                box.information(
                    self, 'Message', '新员工添加成功\n共添加{num}个员工'.format(num=count))
            else:
                box.information(self, 'Message', '没有新员工添加')
            conn.commit()
            conn.close()
            self.show_Name_listWidge()
        else:
            box = QMessageBox()
            box.information(self, 'Message', '请先初始化员工数据')

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

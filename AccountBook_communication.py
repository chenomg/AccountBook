#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: AccountBook_communication.py
#          Desc: use to record the account
#        Author: Jase Chen
#         Email: xxmm@live.cn
#      HomePage: http://jase.im/
#       Version: 1.0.0
#    LastChange: 2018-4-23 22:58:01
#       History:
# =============================================================================
'''
from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QInputDialog, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
import sqlite3
# import logging
import xlrd
import xlwt
import os
import datetime
import re
import sys
from platform import platform
from logo import img as logo_img
from icon import img as icon_img
import base64


class AccountBook_comm(QMainWindow):
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
        self.ui.ltitle_label.setText("百联置业报销登记系统 - 通讯费       ")

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
        self.ui.addStaff_pushButton.clicked.connect(
            self.addStaff_PushButtonClicked)
        # 点击输出按钮然后确定导出
        self.ui.export_pushButton.clicked.connect(self.export_DB_months_all)
        # # Create the Logger
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.DEBUG)

        # # Create the Handler for logging data to a file
        # logger_handler = logging.FileHandler('logging.log')
        # logger_handler.setLevel(logging.DEBUG)

        # # Create a Formatter for formatting the log messages
        # logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # # Add the Formatter to the Handler
        # logger_handler.setFormatter(logger_formatter)

        # # Add the Handler to the Logger
        # self.logger.addHandler(logger_handler)
        # self.logger.info('Completed configuring logger()!')

        # display the logo in the app
        # self.ui.logo_label.setPixmap(QPixmap(basedir+"D:\\code\\AccountBook\\logo.png"))
        tmp_logo = open("tmp_logo.png", "wb+")
        tmp_icon = open("tmp_icon.ico", "wb+")
        tmp_logo.write(base64.b64decode(logo_img))
        tmp_icon.write(base64.b64decode(icon_img))
        tmp_icon.close()
        tmp_logo.close()
        self.ui.logo_label.setPixmap(QPixmap("tmp_logo.png"))
        # 设置程序运行时的图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('tmp_icon.ico'), QtGui.QIcon.Normal)
        self.setWindowIcon(icon)
        os.remove('tmp_logo.png')
        os.remove('tmp_icon.ico')
        self.show()

    def export_get_months_bool_IDs(self, text):
        # return: [bool, IDs_list]
        # 返回bool: 月份是否为完整，还是只是挑选个别月份数据, 完整的话输出整个表格(DATASHEET), 否则输出选择月份的数据(不包含总额，总提取额等数据)
        # 输入包含月份的字符串，例如：‘1-3 5-7,9 2-4  6, 1-8’
        IDs_groups = re.findall(r'(\d+\-\d+)|(\d+)', text)
        IDs_list_str = []
        IDs_set = set()
        IDs_list = []
        isFull_IDs = True

        def full_months():
            full_IDs = []
            for i in range(1, self.get_month()[0] + 1):
                full_IDs.append(i)
            return full_IDs

        for i in IDs_groups:
            for j in i:
                if j:
                    IDs_list_str.append(j)
        # IDs_list_str: ['1-3', '5-7', '9', '2-4', '6', '1-8']
        for item in IDs_list_str:
            if re.findall(r'\-', item):
                id1 = re.findall(r'^\d+', item)[0]
                id2 = re.findall(r'\d+$', item)[0]
                # 检测月份区间的表达是否正确以及id2是否大于当前月份
                if int(id2) >= int(id1) and int(id2) <= self.get_month()[0]:
                    for i in range(int(id1), int(id2) + 1):
                        IDs_set.add(i)
            else:
                IDs_set.add(int(item))
        for i in IDs_set:
            IDs_list.append(i)
        # 判断选择是否为完整月份清单
        if full_months() != IDs_list:
            isFull_IDs = False
        return isFull_IDs, IDs_list

    # 修改为导出全部数据，此段未用
    def export_DB_months_selected(self):
        if self.sqlite_exist():
            text, ok = QInputDialog.getText(self, "Message",
                                            "请输入需要导出数据的月份\n月份:",
                                            QLineEdit.Normal, '1-{}'.format(
                                                self.get_month()[0]))
            if ok and text != '':
                export_months_list = self.export_get_months_bool_IDs(text)
                # todo 待完善
                print(export_months_list)
                # 如果输出整张表格
                if export_months_list[0]:
                    self.export_DB_months_all()
                    box = QMessageBox()
                    box.information(self, 'Message', '数据记录表以及历史记录导出成功！')
                    pass
                # 输出指定月份数据
                else:
                    pass
            else:
                pass
                # box = QMessageBox()
                # box.information(self, 'Message', '已取消~')
        else:
            box = QMessageBox()
            box.information(self, 'Message', '请先初始化员工数据')

    def get_month(self):
        """
        renturn [month_id, month_en, month_cn]
        """
        now = datetime.datetime.now()
        month_en_list = [
            'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP',
            'OCT', 'NOV', 'DEC'
        ]
        month_cn_list = [
            '一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月',
            '十二月'
        ]
        month_id = int(now.month)
        month_en = month_en_list[month_id - 1]
        month_cn = month_cn_list[month_id - 1]
        return month_id, month_en, month_cn

    def export_DB_months_all(self):
        if self.sqlite_exist():
            msgBox = QMessageBox(QMessageBox.Warning, "Message", '需要导出数据吗？',
                                 QMessageBox.NoButton, self)
            msgBox.addButton("Yes!", QMessageBox.AcceptRole)
            msgBox.addButton("No", QMessageBox.RejectRole)
            if msgBox.exec_() == QMessageBox.AcceptRole:
                # 创建表格Excel
                workbook = xlwt.Workbook(encoding='utf-8')
                worksheet = workbook.add_sheet('DATASHEET')
                # 写入excel
                # 参数对应 行, 列, 值
                # 写入标题栏
                worksheet.write(0, 0, label='序号')
                worksheet.write(0, 1, label='姓名')
                worksheet.write(0, 2, label='1月')
                worksheet.write(0, 3, label='2月')
                worksheet.write(0, 4, label='3月')
                worksheet.write(0, 5, label='4月')
                worksheet.write(0, 6, label='5月')
                worksheet.write(0, 7, label='6月')
                worksheet.write(0, 8, label='7月')
                worksheet.write(0, 9, label='8月')
                worksheet.write(0, 10, label='9月')
                worksheet.write(0, 11, label='10月')
                worksheet.write(0, 12, label='11月')
                worksheet.write(0, 13, label='12月')
                worksheet.write(0, 14, label='每月额度')
                worksheet.write(0, 15, label='有效月数')
                worksheet.write(0, 16, label='年度总额')
                worksheet.write(0, 17, label='共支取')
                worksheet.write(0, 18, label='年度剩余')
                # 数据库内数据导出到Excel表格
                conn = sqlite3.connect('db_communication.sqlite')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM DATASHEET")
                infos = cursor.fetchall()
                for info in infos:
                    for j in range(len(info)):
                        worksheet.write(info[0], j, label=info[j])
                # 写入操作记录信息
                worksheet = workbook.add_sheet('HISTORY')
                # 写入excel
                # 参数对应 行, 列, 值
                # 写入标题栏
                worksheet.write(0, 0, label='序号')
                worksheet.write(0, 1, label='时间')
                worksheet.write(0, 2, label='姓名')
                worksheet.write(0, 3, label='提交金额')
                worksheet.write(0, 4, label='共支取')
                worksheet.write(0, 5, label='年度剩余')
                # 数据库内数据导出到Excel表格
                cursor.execute("SELECT * FROM HISTORY")
                infos = cursor.fetchall()
                for info in infos:
                    for j in range(len(info)):
                        worksheet.write(info[0], j, label=info[j])
                cursor.close()
                conn.close()
                updatetime_str = datetime.datetime.now().strftime(
                    "%Y-%m-%d %H-%M-%S")
                export_file_name = '通讯费提取记录%s.xls' % (updatetime_str)
                workbook.save(export_file_name)
                QMessageBox.information(
                    self, "Message",
                    '数据已导出!  详见:\n{}'.format(export_file_name))
                print('Export DATASHEET and HISTORY to excel file succeed')
            else:
                pass
        else:
            box = QMessageBox()
            box.information(self, 'Message', '无数据！')

    def update_info(self):
        # 更新用户信息，包括年度总额，剩余总额和历史记录
        conn = sqlite3.connect('db_communication.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT TOTAL, REMAIN FROM DATASHEET WHERE NAME=?",
                       (self.name_selected, ))
        infos = cursor.fetchall()
        if infos:
            for info in infos:
                self.total_selected = info[0]
                self.remain_selected = info[1]
                self.ui.yearly_lineEdit.setText(str(self.total_selected))
                self.ui.remain_lineEdit.setText(str(round(self.remain_selected, 2)))
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
                string = str(info[0]) + ":于" + str(info[1]) + ', 提交:' + str(
                    info[2]) + ', 共支取:' + str(round(info[3], 2)) + ', 剩余:' + str(
                        round(info[4], 2))
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
        conn = sqlite3.connect('db_communication.sqlite')
        cursor = conn.cursor()
        # 获取现在数据库内数据
        sql = "SELECT " + month + ", EXTRACTED, REMAIN FROM DATASHEET WHERE NAME = '" + name + "'"
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
        conn = sqlite3.connect('db_communication.sqlite')
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
            print("There's no db_communication.sqlite file exists!")

    def submit_Value_Check(self, submit_value, monthly, remain):
        # 用来检查当前输入值是否过大（最大只能超前一个月领取）
        remain_update_minimum = monthly * (
            12 - self.get_month()[0] - self.over_months)
        if remain - submit_value >= remain_update_minimum:
            return True
        else:
            return False

    def submit_PushButtonClicked(self):
        # 提交按钮
        if self.name_selected:
            submit_str = self.ui.submit_lineEdit.text()
            if re.findall(r'^\d*\.?(\d|\d\d)?$', submit_str):
                submit_value = float(self.ui.submit_lineEdit.text())
                if submit_value:
                    # 先判断数据提交后资金提取值是否过大，只能按照最大超前一个月提取交通费，不然给与提醒后再添加
                    conn = sqlite3.connect('db_communication.sqlite')
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
                    if self.submit_Value_Check(submit_value, monthly, remain):
                        # 更新数据库数据
                        self.update_db(
                            name=self.name_selected,
                            month=self.get_month()[1],
                            value=submit_value)
                        self.cancel_name = self.name_selected
                        self.cancel_value = submit_value
                        self.cancel_month = self.get_month()[1]
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
                                month=self.get_month()[1],
                                value=submit_value)
                            self.cancel_name = self.name_selected
                            self.cancel_value = submit_value
                            self.cancel_month = self.get_month()[1]
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
                box.information(self, 'Message', '请检查数据是否正确!。。。')
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
            filename = 'data_txf.xls'
            data = xlrd.open_workbook(filename)
            conn = sqlite3.connect('db_communication.sqlite')
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
        if self.data_txf_xls_exist():
            # 创建员工信息表
            filename = 'data_txf.xls'
            data = xlrd.open_workbook(filename)
            conn = sqlite3.connect('db_communication.sqlite')
            conn.execute(u'''CREATE TABLE DATASHEET(
                ID INT PRIMARY KEY NOT NULL,
                NAME CHAR(10) NOT NULL,
                JAN FLOAT,
                FEB FLOAT,
                MAR FLOAT,
                APR FLOAT,
                MAY FLOAT,
                JUN FLOAT,
                JUL FLOAT,
                AUG FLOAT,
                SEP FLOAT,
                OCT FLOAT,
                NOV FLOAT,
                DEC FLOAT,
                MONTHLY FLOAT NOT NULL,
                MONTHS FLOAT NOT NULL,
                TOTAL FLOAT NOT NULL,
                EXTRACTED FLOAT NOT NULL,
                REMAIN FLOAT NOT NULL);''')
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
            conn = sqlite3.connect('db_communication.sqlite')
            conn.execute(u'''CREATE TABLE HISTORY(
                ID INT PRIMARY KEY NOT NULL,
                UPDATETIME CHAR(30),
                NAME CHAR(10),
                SUBMIT FLOAT,
                EXTRACTED_UPDATE FLOAT,
                REMAIN_UPDATE FLOAT);''')
            conn.commit()
            conn.close()
            # 初始化按钮不可用
            self.ui.init_pushButton.setEnabled(False)
            self.show_Name_listWidge()
            if re.findall(r'^windows.*', self.Platform, re.I):
                import win32con
                import win32api
                # 隐藏数据库文件
                win32api.SetFileAttributes('db_communication.sqlite',
                                           win32con.FILE_ATTRIBUTE_HIDDEN)
            else:
                pass
        else:
            box = QMessageBox()
            box.information(self, 'Message', '未找到员工信息文件:\ndata_txf.xls')

    def get_Name_List(self):
        conn = sqlite3.connect('db_communication.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT NAME FROM DATASHEET')
        names = cursor.fetchall()
        return [name[0] for name in names]

    def sqlite_exist(self):
        path = os.getcwd()
        file_list = os.listdir(path)
        for f in file_list:
            if not os.path.isdir(f):
                if f == 'db_communication.sqlite':
                    return True
        else:
            return False

    def data_txf_xls_exist(self):
        path = os.getcwd()
        file_list = os.listdir(path)
        for f in file_list:
            if not os.path.isdir(f):
                if f == 'data_txf.xls':
                    return True
        else:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = AccountBook_comm()
    sys.exit(app.exec_())

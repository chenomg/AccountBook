#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
ZetCode PyQt5 tutorial

In this example, we create a more
complicated window layout using
the QGridLayout manager.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit,
                             QGridLayout, QApplication, QListWidget,
                             QPushButton)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 创建控件
        name_Label = QLabel('员工姓名:')
        yearly_Label = QLabel('年度总额:')
        now_Lable = QLabel('本次报销:')
        remain_Lable = QLabel('年度剩余:')

        name_List = QListWidget()

        yearly_Edit = QLineEdit()
        now_Edit = QLineEdit()
        remain_Edit = QLineEdit()

        apply_Button = QPushButton('提交数据')
        undo_Button = QPushButton('撤销本次')

        # 布局控件
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(name_Label, 1, 0)
        grid.addWidget(name_List, 1, 1, 3, 1)
        name_List.setFixedsize(50, 30)

        grid.addWidget(yearly_Label, 1, 2)
        grid.addWidget(yearly_Edit, 1, 3)

        grid.addWidget(now_Lable, 2, 2)
        grid.addWidget(now_Edit, 2, 3)

        grid.addWidget(remain_Lable, 3, 2)
        grid.addWidget(remain_Edit, 3, 3)

        grid.addWidget(apply_Button, 1, 4, 2, 1)
        grid.addWidget(undo_Button, 3, 4)
        self.setLayout(grid)

        # set the value in name_List
        name_List.addItem('Grace Gao')
        name_List.addItem('Jase Chen')
        # 设置窗口
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('百联置业交通费出账/记录')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())

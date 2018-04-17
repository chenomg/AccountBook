#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import xlrd
# import xlwt
filename = 'data.xls'
data = xlrd.open_workbook(filename)
conn = sqlite3.connect('db.sqlite')
# conn.execute(u'''CREATE TABLE DATASHEET(
# 序号 INT PRIMARY KEY NOT NULL,
# 姓名 CHAR(10) NOT NULL,
# '1月' INT,
# '2月' INT,
# '3月' INT,
# '4月' INT,
# '5月' INT,
# '6月' INT,
# '7月' INT,
# '8月' INT,
# '9月' INT,
# '10月' INT,
# '11月' INT,
# '12月' INT,
# 每月额度 INT NOT NULL,
# 有效月数 INT NOT NULL,
# 年额度 INT NOT NULL,
# 已支取 INT NOT NULL,
# 剩余额度 INT NOT NULL);''')
table = data.sheets()[0]
nrows = table.nrows
# for i in range(nrows - 1):
# insertDatas = table.row_values(i + 1)
# conn.execute('''INSERT INTO DATASHEET(
# 序号,姓名,"1月",'2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',每月额度,有效月数,年额度,已支取,剩余额度
# ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
# (insertDatas))
cursor = conn.cursor()
results = cursor.execute('SELECT 姓名 FROM DATASHEET;')
names = cursor.fetchall()
print(names)
conn.commit()
conn.close()

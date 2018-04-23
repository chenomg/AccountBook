#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3


def get_info():
    # 更新用户信息，包括年度总额，剩余总额和历史记录
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DATASHEET")
    infos = cursor.fetchall()
    print(infos)


if __name__ == "__main__":
    get_info()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import Frame


class AccountBook():
    def __init__(self):
        self.window = tk.Tk()
        # 设定主窗口
        self.window.title('AccountBook')
        self.window.geometry('600x400+200+200')
        self.window.resizable(width='FALSE', height='FALSE')
        # create all of the main containers
        self.top_frame = Frame(
            self.window, bg='white', width=600, height=100, pady=5)
        self.mid_L_frame = Frame(self.window, bg='white', width=150, height=80)
        self.mid_M_frame = Frame(
            self.window, bg='white', width=150, height=120)
        self.mid_R_frame = Frame(
            self.window, bg='lavender', width=150, height=120)
        self.bottom_frame = Frame(self.window, bg='red', width=600, height=180)
        # layout all of the main containers
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky='S')
        self.mid_L_frame.grid(row=1, column=0, padx=00, pady=10, sticky='N')
        self.mid_M_frame.grid(row=1, column=1, padx=00, pady=10, sticky='N')
        self.mid_R_frame.grid(row=1, column=2, padx=20, pady=10, sticky='N')
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky='NW')
        # create the widgets for the top_frame
        self.title_label = tk.Label(
            self.top_frame, text='百联置业交通费出账/记录', font=('Arial', 25))
        # layout the widgets in the top_frame
        self.title_label.grid(
            row=0, column=0, columnspan=4, pady=10, sticky='E')
        # create the widgets for the mid_L_frame
        self.name_label = tk.Label(
            self.mid_L_frame, text='员工姓名', font=('Arial', 17))
        var = tk.StringVar()
        self.name_list = tk.Listbox(
            self.mid_L_frame, bd=1, height=6, width=12, listvariable=var)
        var.set(('test1', 'test2'))
        # layout the widgets in the mid_L_frame
        self.name_label.grid(row=0, column=0, padx=30, pady=00, sticky='NW')
        self.name_list.grid(row=1, column=0, padx=30, pady=00, sticky='E')
        # create the widgets for the mid_M_frame
        self.yearly_total_label = tk.Label(
            self.mid_M_frame, text='年度总额:', font=('Arial', 17))
        self.now_lable = tk.Label(
            self.mid_M_frame, text='本次报销:', font=('Arial', 17))
        self.remain_lable = tk.Label(
            self.mid_M_frame, text='年度剩余', font=('Arial', 17))
        self.yearly_entry = tk.Entry(self.mid_M_frame, width=12)
        self.now_entry = tk.Entry(self.mid_M_frame, width=12)
        self.remain_entry = tk.Entry(self.mid_M_frame, width=12)
        # layout the widgets in the mid_M_frame
        self.yearly_total_label.grid(row=0, column=0, pady=10)
        self.now_lable.grid(row=1, column=0, pady=10)
        self.remain_lable.grid(row=2, column=0, pady=10)
        self.yearly_entry.grid(row=0, column=1)
        self.now_entry.grid(row=1, column=1)
        self.remain_entry.grid(row=2, column=1)
        # 运行窗口
        self.window.mainloop()


def main():
    # 运行窗口程序
    window = AccountBook()


if __name__ == "__main__":
    main()

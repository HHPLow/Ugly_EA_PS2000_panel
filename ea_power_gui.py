#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#

import sys
from ea_psu_controller import PsuEA
import configparser
import time
import threading
import os
import ea_power_gui_support
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

from tkinter import *

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    ea_power_gui_support.init(root, top)
    root.mainloop()

w = None
current_a = 0.0
current_v = 0.0

def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    ea_power_gui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    vol = 0.0
    current = 0.0
    status = True
    changed = False
    power_status = False
    tsk = []

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.info_a = StringVar()
        self.info_v = StringVar()

        top.geometry("600x450+719+372")
        top.minsize(120, 1)
        top.maxsize(3124, 1908)
        top.resizable(1,  1)
        top.title("EA Power Panel")
        top.configure(background="#d9d9d9")

        self.Button_plus_1V = tk.Button(top)
        self.Button_plus_1V.place(relx=0.1, rely=0.044, height=28, width=49)
        self.Button_plus_1V.configure(activebackground="#ececec")
        self.Button_plus_1V.configure(activeforeground="#000000")
        self.Button_plus_1V.configure(background="#d9d9d9")
        self.Button_plus_1V.configure(disabledforeground="#a3a3a3")
        self.Button_plus_1V.configure(foreground="#000000")
        self.Button_plus_1V.configure(highlightbackground="#d9d9d9")
        self.Button_plus_1V.configure(highlightcolor="black")
        self.Button_plus_1V.configure(pady="0")
        self.Button_plus_1V.configure(text='''+1V''')
        self.Button_plus_1V.configure(command=self.power_plus_1_cb)

        self.Button1_plus_0_1V = tk.Button(top)
        self.Button1_plus_0_1V.place(relx=0.233, rely=0.044, height=28, width=49)

        self.Button1_plus_0_1V.configure(activebackground="#ececec")
        self.Button1_plus_0_1V.configure(activeforeground="#000000")
        self.Button1_plus_0_1V.configure(background="#d9d9d9")
        self.Button1_plus_0_1V.configure(disabledforeground="#a3a3a3")
        self.Button1_plus_0_1V.configure(foreground="#000000")
        self.Button1_plus_0_1V.configure(highlightbackground="#d9d9d9")
        self.Button1_plus_0_1V.configure(highlightcolor="black")
        self.Button1_plus_0_1V.configure(pady="0")
        self.Button1_plus_0_1V.configure(text='''+0.1V''')
        self.Button1_plus_0_1V.configure(command=self.power_plus_0_1_cb)

        self.Button_sub_0_1V = tk.Button(top)
        self.Button_sub_0_1V.place(relx=0.233, rely=0.289, height=28, width=49)
        self.Button_sub_0_1V.configure(activebackground="#ececec")
        self.Button_sub_0_1V.configure(activeforeground="#000000")
        self.Button_sub_0_1V.configure(background="#d9d9d9")
        self.Button_sub_0_1V.configure(disabledforeground="#a3a3a3")
        self.Button_sub_0_1V.configure(foreground="#000000")
        self.Button_sub_0_1V.configure(highlightbackground="#d9d9d9")
        self.Button_sub_0_1V.configure(highlightcolor="black")
        self.Button_sub_0_1V.configure(pady="0")
        self.Button_sub_0_1V.configure(text='''-0.1V''')
        self.Button_sub_0_1V.configure(command=self.power_sub_0_1_cb)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Button_sub_1V = tk.Button(top)
        self.Button_sub_1V.place(relx=0.1, rely=0.289, height=28, width=49)
        self.Button_sub_1V.configure(activebackground="#ececec")
        self.Button_sub_1V.configure(activeforeground="#000000")
        self.Button_sub_1V.configure(background="#d9d9d9")
        self.Button_sub_1V.configure(disabledforeground="#a3a3a3")
        self.Button_sub_1V.configure(foreground="#000000")
        self.Button_sub_1V.configure(highlightbackground="#d9d9d9")
        self.Button_sub_1V.configure(highlightcolor="black")
        self.Button_sub_1V.configure(pady="0")
        self.Button_sub_1V.configure(text='''-1V''')
        self.Button_sub_1V.configure(command=self.power_sub_1_cb)


        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.317, rely=0.178, height=33, width=37)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''V''')

        self.Label1_1 = tk.Label(top)
        self.Label1_1.place(relx=0.683, rely=0.178, height=33, width=37)
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(activeforeground="black")
        self.Label1_1.configure(background="#d9d9d9")
        self.Label1_1.configure(disabledforeground="#a3a3a3")
        self.Label1_1.configure(foreground="#000000")
        self.Label1_1.configure(highlightbackground="#d9d9d9")
        self.Label1_1.configure(highlightcolor="black")
        self.Label1_1.configure(text='''A''')

        self.Label_vol_text = tk.Label(top)
        self.Label_vol_text.place(relx=0.1, rely=0.156, height=30, width=100)
        self.Label_vol_text.configure(activebackground="#f9f9f9")
        self.Label_vol_text.configure(activeforeground="black")
        self.Label_vol_text.configure(background="#d9d9d9")
        self.Label_vol_text.configure(disabledforeground="#a3a3a3")
        self.Label_vol_text.configure(foreground="#000000")
        self.Label_vol_text.configure(highlightbackground="#d9d9d9")
        self.Label_vol_text.configure(highlightcolor="black")
        # self.Label_vol_text.configure(textvariable=str(self.vol))
        self.info_v.set(str(self.vol))
        self.Label_vol_text.configure(textvariable=self.info_v)

        self.Label_a_text = tk.Label(top)
        self.Label_a_text.place(relx=0.467, rely=0.156, height=30, width=100)
        self.Label_a_text.configure(activebackground="#f9f9f9")
        self.Label_a_text.configure(activeforeground="black")
        self.Label_a_text.configure(background="#d9d9d9")
        self.Label_a_text.configure(disabledforeground="#a3a3a3")
        self.Label_a_text.configure(foreground="#000000")
        self.Label_a_text.configure(highlightbackground="#d9d9d9")
        self.Label_a_text.configure(highlightcolor="black")
        # self.Label_a_text.configure(textvariable=str(self.current))
        self.info_a.set(str(self.current))
        self.Label_a_text.configure(textvariable=self.info_a)

        self.Button_ON = tk.Button(top)
        self.Button_ON.place(relx=0.833, rely=0.178, height=28, width=49)
        self.Button_ON.configure(activebackground="#ececec")
        self.Button_ON.configure(activeforeground="#000000")
        self.Button_ON.configure(background="#d9d9d9")
        self.Button_ON.configure(disabledforeground="#a3a3a3")
        self.Button_ON.configure(foreground="#000000")
        self.Button_ON.configure(highlightbackground="#d9d9d9")
        self.Button_ON.configure(highlightcolor="black")
        self.Button_ON.configure(pady="0")
        self.Button_ON.configure(text='''ON''')
        self.Button_ON.configure(command=self.power_on_cb)

        self.Button_OFF = tk.Button(top)
        self.Button_OFF.place(relx=0.833, rely=0.267, height=28, width=49)
        self.Button_OFF.configure(activebackground="#ececec")
        self.Button_OFF.configure(activeforeground="#000000")
        self.Button_OFF.configure(background="#d9d9d9")
        self.Button_OFF.configure(disabledforeground="#a3a3a3")
        self.Button_OFF.configure(foreground="#000000")
        self.Button_OFF.configure(highlightbackground="#d9d9d9")
        self.Button_OFF.configure(highlightcolor="black")
        self.Button_OFF.configure(pady="0")
        self.Button_OFF.configure(text='''OFF''')
        self.Button_OFF.configure(command=self.power_off_cb)

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.283, rely=0.4,  relwidth=0.333)

        self.TSeparator2 = ttk.Separator(top)
        self.TSeparator2.place(relx=0.283, rely=0.556,  relwidth=0.333)

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.017, rely=0.422, height=23, width=80)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''ON OFF Test''')

        self.Label2_1 = tk.Label(top)
        self.Label2_1.place(relx=0.0, rely=0.578, height=23, width=100)
        self.Label2_1.configure(activebackground="#f9f9f9")
        self.Label2_1.configure(activeforeground="black")
        self.Label2_1.configure(background="#d9d9d9")
        self.Label2_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1.configure(foreground="#000000")
        self.Label2_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1.configure(highlightcolor="black")
        self.Label2_1.configure(text='''V Change Test''')

        self.Button_ON_OFF_RUN = tk.Button(top)
        self.Button_ON_OFF_RUN.place(relx=0.8, rely=0.489, height=28, width=38)
        self.Button_ON_OFF_RUN.configure(activebackground="#ececec")
        self.Button_ON_OFF_RUN.configure(activeforeground="#000000")
        self.Button_ON_OFF_RUN.configure(background="#d9d9d9")
        self.Button_ON_OFF_RUN.configure(disabledforeground="#a3a3a3")
        self.Button_ON_OFF_RUN.configure(foreground="#000000")
        self.Button_ON_OFF_RUN.configure(highlightbackground="#d9d9d9")
        self.Button_ON_OFF_RUN.configure(highlightcolor="black")
        self.Button_ON_OFF_RUN.configure(pady="0")
        self.Button_ON_OFF_RUN.configure(text='''RUN''')
        self.Button_ON_OFF_RUN.configure(command=self.power_on_off_test)

        self.Text_SLEEP_TIME = tk.Text(top)
        self.Text_SLEEP_TIME.place(relx=0.15, rely=0.467, relheight=0.071, relwidth=0.157)
        self.Text_SLEEP_TIME.configure(background="white")
        self.Text_SLEEP_TIME.configure(cursor="fleur")
        self.Text_SLEEP_TIME.configure(font="TkTextFont")
        self.Text_SLEEP_TIME.configure(foreground="black")
        self.Text_SLEEP_TIME.configure(highlightbackground="#d9d9d9")
        self.Text_SLEEP_TIME.configure(highlightcolor="black")
        self.Text_SLEEP_TIME.configure(insertbackground="black")
        self.Text_SLEEP_TIME.configure(selectbackground="blue")
        self.Text_SLEEP_TIME.configure(selectforeground="white")
        self.Text_SLEEP_TIME.configure(wrap="word")

        self.Label_time = tk.Label(top)
        self.Label_time.place(relx=0.01, rely=0.467, height=23, width=66)
        self.Label_time.configure(background="#d9d9d9")
        self.Label_time.configure(cursor="fleur")
        self.Label_time.configure(disabledforeground="#a3a3a3")
        self.Label_time.configure(foreground="#000000")
        self.Label_time.configure(text='''Sleep time:''')

        self.Text_ON_OFF_COUNT = tk.Text(top)
        self.Text_ON_OFF_COUNT.place(relx=0.45, rely=0.467, relheight=0.071, relwidth=0.157)
        self.Text_ON_OFF_COUNT.configure(background="white")
        self.Text_ON_OFF_COUNT.configure(cursor="fleur")
        self.Text_ON_OFF_COUNT.configure(font="TkTextFont")
        self.Text_ON_OFF_COUNT.configure(foreground="black")
        self.Text_ON_OFF_COUNT.configure(highlightbackground="#d9d9d9")
        self.Text_ON_OFF_COUNT.configure(highlightcolor="black")
        self.Text_ON_OFF_COUNT.configure(insertbackground="black")
        self.Text_ON_OFF_COUNT.configure(selectbackground="blue")
        self.Text_ON_OFF_COUNT.configure(selectforeground="white")
        self.Text_ON_OFF_COUNT.configure(wrap="word")

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.367, rely=0.489, height=23, width=43)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(cursor="fleur")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Count:''')

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.1, rely=0.644, height=28, width=79)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(cursor="fleur")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Voltage''')

        self.Button2_1 = tk.Button(top)
        self.Button2_1.place(relx=0.333, rely=0.644, height=28, width=79)
        self.Button2_1.configure(activebackground="#ececec")
        self.Button2_1.configure(activeforeground="#000000")
        self.Button2_1.configure(background="#d9d9d9")
        self.Button2_1.configure(cursor="fleur")
        self.Button2_1.configure(disabledforeground="#a3a3a3")
        self.Button2_1.configure(foreground="#000000")
        self.Button2_1.configure(highlightbackground="#d9d9d9")
        self.Button2_1.configure(highlightcolor="black")
        self.Button2_1.configure(pady="0")
        self.Button2_1.configure(text='''Time''')

        self.Voltage_1 = tk.Text(top)
        self.Voltage_1.place(relx=0.1, rely=0.733, relheight=0.049, relwidth=0.123)
        self.Voltage_1.configure(background="white")
        self.Voltage_1.configure(font="TkTextFont")
        self.Voltage_1.configure(foreground="black")
        self.Voltage_1.configure(highlightbackground="#d9d9d9")
        self.Voltage_1.configure(highlightcolor="black")
        self.Voltage_1.configure(insertbackground="black")
        self.Voltage_1.configure(selectbackground="blue")
        self.Voltage_1.configure(selectforeground="white")
        self.Voltage_1.configure(wrap="word")

        self.Time_1 = tk.Text(top)
        self.Time_1.place(relx=0.333, rely=0.733, relheight=0.049
                          , relwidth=0.123)
        self.Time_1.configure(background="white")
        self.Time_1.configure(font="TkTextFont")
        self.Time_1.configure(foreground="black")
        self.Time_1.configure(highlightbackground="#d9d9d9")
        self.Time_1.configure(highlightcolor="black")
        self.Time_1.configure(insertbackground="black")
        self.Time_1.configure(selectbackground="blue")
        self.Time_1.configure(selectforeground="white")
        self.Time_1.configure(wrap="word")

        self.Voltage_2 = tk.Text(top)
        self.Voltage_2.place(relx=0.1, rely=0.8, relheight=0.049, relwidth=0.123)
        self.Voltage_2.configure(background="white")
        self.Voltage_2.configure(font="TkTextFont")
        self.Voltage_2.configure(foreground="black")
        self.Voltage_2.configure(highlightbackground="#d9d9d9")
        self.Voltage_2.configure(highlightcolor="black")
        self.Voltage_2.configure(insertbackground="black")
        self.Voltage_2.configure(selectbackground="blue")
        self.Voltage_2.configure(selectforeground="white")
        self.Voltage_2.configure(wrap="word")

        self.Time_2 = tk.Text(top)
        self.Time_2.place(relx=0.333, rely=0.8, relheight=0.049, relwidth=0.123)

        self.Time_2.configure(background="white")
        self.Time_2.configure(font="TkTextFont")
        self.Time_2.configure(foreground="black")
        self.Time_2.configure(highlightbackground="#d9d9d9")
        self.Time_2.configure(highlightcolor="black")
        self.Time_2.configure(insertbackground="black")
        self.Time_2.configure(selectbackground="blue")
        self.Time_2.configure(selectforeground="white")
        self.Time_2.configure(wrap="word")

        self.Voltage_3 = tk.Text(top)
        self.Voltage_3.place(relx=0.1, rely=0.867, relheight=0.049, relwidth=0.123)

        self.Voltage_3.configure(background="white")
        self.Voltage_3.configure(font="TkTextFont")
        self.Voltage_3.configure(foreground="black")
        self.Voltage_3.configure(highlightbackground="#d9d9d9")
        self.Voltage_3.configure(highlightcolor="black")
        self.Voltage_3.configure(insertbackground="black")
        self.Voltage_3.configure(selectbackground="blue")
        self.Voltage_3.configure(selectforeground="white")
        self.Voltage_3.configure(wrap="word")

        self.Time_3 = tk.Text(top)
        self.Time_3.place(relx=0.333, rely=0.867, relheight=0.049
                          , relwidth=0.123)
        self.Time_3.configure(background="white")
        self.Time_3.configure(font="TkTextFont")
        self.Time_3.configure(foreground="black")
        self.Time_3.configure(highlightbackground="#d9d9d9")
        self.Time_3.configure(highlightcolor="black")
        self.Time_3.configure(insertbackground="black")
        self.Time_3.configure(selectbackground="blue")
        self.Time_3.configure(selectforeground="white")
        self.Time_3.configure(wrap="word")

        self.Voltage_4 = tk.Text(top)
        self.Voltage_4.place(relx=0.1, rely=0.933, relheight=0.049, relwidth=0.123)

        self.Voltage_4.configure(background="white")
        self.Voltage_4.configure(font="TkTextFont")
        self.Voltage_4.configure(foreground="black")
        self.Voltage_4.configure(highlightbackground="#d9d9d9")
        self.Voltage_4.configure(highlightcolor="black")
        self.Voltage_4.configure(insertbackground="black")
        self.Voltage_4.configure(selectbackground="blue")
        self.Voltage_4.configure(selectforeground="white")
        self.Voltage_4.configure(wrap="word")

        self.Time_4 = tk.Text(top)
        self.Time_4.place(relx=0.333, rely=0.933, relheight=0.049, relwidth=0.123)
        self.Time_4.configure(background="white")
        self.Time_4.configure(font="TkTextFont")
        self.Time_4.configure(foreground="black")
        self.Time_4.configure(highlightbackground="#d9d9d9")
        self.Time_4.configure(highlightcolor="black")
        self.Time_4.configure(insertbackground="black")
        self.Time_4.configure(selectbackground="blue")
        self.Time_4.configure(selectforeground="white")
        self.Time_4.configure(wrap="word")

        self.Button_voltage_change_run = tk.Button(top)
        self.Button_voltage_change_run.place(relx=0.8, rely=0.844, height=28, width=38)
        self.Button_voltage_change_run.configure(activebackground="#ececec")
        self.Button_voltage_change_run.configure(activeforeground="#000000")
        self.Button_voltage_change_run.configure(background="#d9d9d9")
        self.Button_voltage_change_run.configure(disabledforeground="#a3a3a3")
        self.Button_voltage_change_run.configure(foreground="#000000")
        self.Button_voltage_change_run.configure(highlightbackground="#d9d9d9")
        self.Button_voltage_change_run.configure(highlightcolor="black")
        self.Button_voltage_change_run.configure(pady="0")
        self.Button_voltage_change_run.configure(text='''RUN''')
        self.Button_voltage_change_run.configure(command=self.power_program_test)

        self.Label3_1 = tk.Label(top)
        self.Label3_1.place(relx=0.56, rely=0.736, height=23, width=43)
        self.Label3_1.configure(activebackground="#f9f9f9")
        self.Label3_1.configure(activeforeground="black")
        self.Label3_1.configure(background="#d9d9d9")
        self.Label3_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1.configure(foreground="#000000")
        self.Label3_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1.configure(highlightcolor="black")
        self.Label3_1.configure(text='''Count:''')

        self.Voltage_change_count = tk.Text(top)
        self.Voltage_change_count.place(relx=0.633, rely=0.711, relheight=0.071
                                        , relwidth=0.157)
        self.Voltage_change_count.configure(background="white")
        self.Voltage_change_count.configure(font="TkTextFont")
        self.Voltage_change_count.configure(foreground="black")
        self.Voltage_change_count.configure(highlightbackground="#d9d9d9")
        self.Voltage_change_count.configure(highlightcolor="black")
        self.Voltage_change_count.configure(insertbackground="black")
        self.Voltage_change_count.configure(selectbackground="blue")
        self.Voltage_change_count.configure(selectforeground="white")
        self.Voltage_change_count.configure(wrap="word")

        self.Label_status = tk.Label(top)
        self.Label_status.place(relx=0.533, rely=0.044, height=23, width=100)
        self.Label_status.configure(activebackground="#f9f9f9")
        self.Label_status.configure(activeforeground="black")
        self.Label_status.configure(background="#d9d9d9")
        self.Label_status.configure(disabledforeground="#a3a3a3")
        self.Label_status.configure(foreground="#000000")
        self.Label_status.configure(highlightbackground="#d9d9d9")
        self.Label_status.configure(highlightcolor="black")
        self.Label_status.configure(text='''IDEL...:''')

        self.Label_test_status = tk.Label(top)
        self.Label_test_status.place(relx=0.533, rely=0.084, height=23, width=300)
        self.Label_test_status.configure(activebackground="#f9f9f9")
        self.Label_test_status.configure(activeforeground="black")
        self.Label_test_status.configure(background="#d9d9d9")
        self.Label_test_status.configure(disabledforeground="#a3a3a3")
        self.Label_test_status.configure(foreground="#000000")
        self.Label_test_status.configure(highlightbackground="#d9d9d9")
        self.Label_test_status.configure(highlightcolor="black")
        self.Label_test_status.configure(text='''IDEL...:''')
        T = threading.Thread(target=self.update_value)
        T.start()
        self.tsk.append(T)

        Button(root, text="Quit", command=root.destroy).pack()

    def destroy_all(self):
        self.Label_status.configure(text="Exit......")
        self.status = False
        psu.close(True, True)
        for tt in self.tsk:
            tt.stop()
            tt.join()
        destroy_Toplevel1()

    def update_value(self):
        self.Label_status.configure(text="Runing......")
        last_status = self.power_status
        while self.status:
            time.sleep(0.2)

            if self.changed:
                psu.set_voltage(self.vol)
                self.changed = False
            time.sleep(0.1)
            if last_status != self.power_status:
                last_status = self.power_status
                if self.power_status:
                    psu.output_on()
                    self.Label_status.configure(text="POWER ON..")
                else:
                    psu.output_off()
                    self.Label_status.configure(text="POWER OFF..")

            self.vol = round(psu.get_voltage(), 3)
            time.sleep(0.1)
            self.current = round(psu.get_current(), 3)
            self.info_v.set(str(self.vol))
            self.info_a.set(str(self.current))

            # self.Label_vol_text.configure(text=str(self.vol))
            # self.Label_a_text.configure(text=str(self.current))

    def power_plus_1_cb(self):
        self.vol += 1
        self.changed = True

    def power_plus_0_1_cb(self):
        self.vol += 0.1
        self.changed = True

    def power_sub_1_cb(self):
        self.vol -= 1
        self.changed = True

    def power_sub_0_1_cb(self):
        self.vol = float(self.vol) - 0.2
        self.changed = True

    def power_on_cb(self):
        self.power_status = True

    def power_off_cb(self):
        self.power_status = False

    def power_on_off_test_thread(self):
        self.Label_test_status.configure(text="Running on/off test...")
        cycle_count = int(self.Text_ON_OFF_COUNT.get("1.0", END))
        sleep_time = int(self.Text_SLEEP_TIME.get("1.0", END))
        count = 0
        if cycle_count != 0:
            while cycle_count != 0:
                cycle_count -= 1
                count += 1
                self.Label_test_status.configure(text="Running program test,count {0}...".format(count))
                self.power_status = True
                time.sleep(sleep_time)
                self.power_status = False
                time.sleep(sleep_time)
        else:
            while True:
                    count += 1
                    self.Label_test_status.configure(text="Running program test,count {0}...".format(count))
                    self.power_status = True
                    time.sleep(sleep_time)
                    self.power_status = False
                    time.sleep(sleep_time)
        self.Label_test_status.configure(text="Running on/off test DONE...")

    def power_on_off_test(self):
        T2 = threading.Thread(target=self.power_on_off_test_thread)
        T2.start()
        self.tsk.append(T2)

    def power_program_test_thread(self):
        self.Label_test_status.configure(text="Running program test...")
        vol_list = []
        time_list = []
        self.power_status = True
        if len(self.Voltage_1.get("1.0", END)) != 1:
            vol_list.append(float(self.Voltage_1.get("1.0", END)))
            print(self.Voltage_1.get("1.0", END))
        if len(self.Voltage_2.get("1.0", END)) != 1:
            vol_list.append(float(self.Voltage_2.get("1.0", END)))
        if len(self.Voltage_3.get("1.0", END)) != 1:
            vol_list.append(float(self.Voltage_3.get("1.0", END)))
        if len(self.Voltage_4.get("1.0", END)) != 1:
            vol_list.append(float(self.Voltage_4.get("1.0", END)))

        if len(self.Time_1.get("1.0", END)) != 1:
            time_list.append(int(self.Time_1.get("1.0", END)))
        if len(self.Time_2.get("1.0", END)) != 1:
            time_list.append(int(self.Time_2.get("1.0", END)))
        if len(self.Time_3.get("1.0", END)) != 1:
            time_list.append(int(self.Time_3.get("1.0", END)))
        if len(self.Time_4.get("1.0", END)) != 1:
            time_list.append(int(self.Time_4.get("1.0", END)))
        cycle_count = int(self.Voltage_change_count.get("1.0", END))
        count = 0
        if cycle_count != 0:
            while cycle_count != 0:
                cycle_count -= 1
                count += 1
                index = 0
                self.Label_test_status.configure(text="Running program test,count {0}...".format(count))
                for vol in vol_list:
                    psu.set_voltage(vol)
                    time.sleep(time_list[index])
                    index += 1
        else:
            while True:
                index = 0
                count += 1
                self.Label_test_status.configure(text="Running program test,count {0}...".format(count))
                for vol in vol_list:
                    psu.set_voltage(vol)
                    time.sleep(time_list[index])
                    index += 1
        self.Label_test_status.configure(text="Running program DONE...")

    def power_program_test(self):
        T3 = threading.Thread(target=self.power_program_test_thread)
        T3.start()
        self.tsk.append(T3)

if __name__ == '__main__':
    path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(path))
    config = configparser.ConfigParser()
    config.read("EA_POWER_CONFIG.ini")

    cycle_count = config.getint("DEVICE", "power_cycle_count")
    power_v_config_count = config.getint("DEVICE", "power_v_count")
    psu = PsuEA(comport=str(config.get("DEVICE", "port")))
    psu.set_ovp(18)
    psu.set_ocp(10)
    # psu.remote_on()
    vp_start_gui()




# Simply Good Scanner (SGS)
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import validators
import webbrowser
import pyperclip

# Global variables
data = []

def work(num):
    cap = cv2.VideoCapture(num, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)

    try:
        while True:
            success, img = cap.read()
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (0,255,0), 5)
                pts2 = barcode.rect
                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                data.append(myData)
            cv2.imshow('Result', img)
            cv2.waitKey(1)
    except KeyboardInterrupt as e:
        cap.release()
        cv2.destroyAllWindows()

def startFunction():
    value = clicked.get()
    if value == "Select Source":
        messagebox.showerror("Source Error", "Select a source before clicking start you fool")
    elif value == "External Camera":
        work(1)
    elif value == "Laptop Camera":
        work(0)


def openFunction():
    dataList = list(set(data))
    for d in dataList:
        if validators.url(d):
            webbrowser.open(d)


def copyFunction():
    dataList = list(set(data))
    pyperclip.copy('\n'.join(dataList))    


def showFunction():
    dataList = list(set(data))
    messagebox.showinfo("Output", '\n'.join(dataList))


def getOption(s):
    clicked.set(s)

# -- Windows only configuration --
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# -- End Windows only configuration --

root = tk.Tk()

# This is the section of code which creates the main window
root.geometry("600x550")
root.title("Simply Good Scanner")
root.resizable(0, 0)

# Title
ttk.Label(root, text='Simply Good Scanner',
          font=("Comic Sans MS", 30)).place(x=100, y=20)

# Source Label
ttk.Label(root, text='Source', font=("Comic Sans MS", 20)).place(x=80, y=110)

# Options

options = ["Select Source", "Laptop Camera", "External Camera"]
clicked = tk.StringVar(value=options[0])

# Create Dropdown menu
drop = tk.OptionMenu(root, clicked, *options, command=getOption)
drop.place(x=320, y=100)
drop.config(font=("Comic Sans MS", 20))
menu = root.nametowidget(drop.menuname)
menu.config(font=("Comic Sans MS", 14))

# start button
startBtn = tk.Button(root,
                     text='Start',
                     command=startFunction,
                     font=("Comic Sans MS", 20))
startBtn.place(x=250, y=200)

# Open in browser button
openBtn = tk.Button(root,
                    text='Open only urls',
                    command=openFunction,
                    font=("Comic Sans MS", 20))
openBtn.place(x=200, y=280)
# Copy to clipboard button
copyBtn = tk.Button(root,
                    text='Copy to clipboard',
                    command=copyFunction,
                    font=("Comic Sans MS", 20))
copyBtn.place(x=180, y=360)
# Show data button
showBtn = tk.Button(root,
                    text='Show Data',
                    command=showFunction,
                    font=("Comic Sans MS", 20))
showBtn.place(x=220, y=440)

root.mainloop()
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmCrawl.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter
tk = tkinter.Tk()
from tkinter import messagebox
import threading
import enum
from bs4 import BeautifulSoup
import urllib.request
import requests
import shutil
import os

import re
class STATUS(enum.Enum):
    Ready = 1
    Running = 2
stt = STATUS.Ready
# count = 0
def giv_url(url):
    # print(url)
    try:
        html_text = requests.get(url).text
    except:
        return
    soup = BeautifulSoup(html_text, 'lxml')
    sub_url =[url]
    for link in soup.find_all('a'):
        sub_link = link.get('href')
        if sub_link:
            if sub_link[:4] != 'http':
                if sub_link[:2] == '//':
                    sub_link = sub_link[1:]
                if sub_link[0] != '/':
                    sub_link = '/' + sub_link
                # print(link)
                sub_link = url + sub_link
            if not sub_link in sub_url:
                sub_url.append(sub_link)
            print(sub_link)
    return sub_url

def crawl(url,data_type):
    global stt
    # global count
    # print(count, url)
    try:  
        html = str(urllib.request.urlopen(url).read())
    except:
        return
    links = re.findall(r'http[s]?://[a-zA-Z0-9-\._~/?#@&=]*\.'+data_type, html)
    for link in links:
        if stt == STATUS.Ready:
            break
        os.system("you-get "+str(link)+" -a -o Data")

    # count +=1
def process(url,data_type):
    global stt
    # print(url)
    stt = STATUS.Running
    if url[-1] == '/':
        url = url[:-1]
    os.system("mkdir Data")
    lst_url = giv_url(url)
    print(lst_url)
    
    for link in lst_url:
        for tp in data_type:
            print('------------------'+ tp +'-------------------')
            if stt == STATUS.Ready:
                break
            crawl(link,tp)
        print("Done!!")
    stt = STATUS.Ready

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(667, 403)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl1 = QtWidgets.QLabel(self.centralwidget)
        self.lbl1.setGeometry(QtCore.QRect(90, 80, 331, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl1.setFont(font)
        self.lbl1.setObjectName("lbl1")

        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(190, 270, 91, 31))
        self.btnStart.setObjectName("btnStart")
        self.btnStart.clicked.connect(self.start)

        self.btnStop = QtWidgets.QPushButton(self.centralwidget)
        self.btnStop.setGeometry(QtCore.QRect(340, 270, 91, 31))
        self.btnStop.setObjectName("btnStop")
        self.btnStop.clicked.connect(self.stop)

        self.txtUrl = QtWidgets.QTextEdit(self.centralwidget)
        self.txtUrl.setGeometry(QtCore.QRect(150, 120, 331, 41))
        self.txtUrl.setObjectName("txtUrl")

        self.lbl1_2 = QtWidgets.QLabel(self.centralwidget)
        self.lbl1_2.setGeometry(QtCore.QRect(170, 180, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl1_2.setFont(font)
        self.lbl1_2.setObjectName("lbl1_2")
        self.txtType = QtWidgets.QTextEdit(self.centralwidget)
        self.txtType.setGeometry(QtCore.QRect(300, 190, 111, 31))
        self.txtType.setObjectName("txtType")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 667, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Crawler Tool"))
        self.lbl1.setText(_translate("MainWindow", "Please enter url you want to crawl:"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.btnStop.setText(_translate("MainWindow", "Stop"))
        self.lbl1_2.setText(_translate("MainWindow", "Data type :"))
    def start(self):
        url=self.txtUrl.toPlainText()
        # print(url)
        data_type = self.txtType.toPlainText()
        if not url:
            tk.withdraw()
            messagebox.showwarning("Warning","Please enter URL!!")
        elif not data_type:
            tk.withdraw()
            messagebox.showwarning("Warning","Please enter Data type!!")
        elif url[:4] != 'http':
                tk.withdraw()
                messagebox.showwarning("Warning","Please enter HTTP URL!!")
        else:
            data_type = data_type.split(' ')
            for i in range(len(data_type)):
                if data_type[i][0] == '.':
                    data_type[i] = data_type[i][1:]
            t = threading.Thread(target=process,args=[url,data_type])
            t.start()
    def stop(self):
        global stt
        stt = STATUS.Ready

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

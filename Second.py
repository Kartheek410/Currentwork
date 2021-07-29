# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Second.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import xmltodict, json
import zipfile
from PIL import Image
from Postcuring import Ui_PostCuring
import time
import mainmotor

class Ui_SecondWindow(object):

    def openWindow2(self): #Calling the Postcuring window on SecondWindow
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_PostCuring()
        self.ui.setupUi(self.window2)
        self.window2.show()
    def setupUi(self, SecondWindow):
        self.SecondWindow = SecondWindow #link to the on_close function
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(1024, 600)
        SecondWindow.setMinimumSize(QtCore.QSize(1024, 600))
        SecondWindow.setMaximumSize(QtCore.QSize(1024, 600))
        SecondWindow.setStyleSheet("background-color: rgb(60, 181, 228);")
        SecondWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 2, 1021, 81))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Selectjob = QtWidgets.QPushButton(self.centralwidget)
        self.Selectjob.setGeometry(QtCore.QRect(1, 120, 340, 240))
        self.Selectjob.setStyleSheet("background-color: rgb(60, 181, 228); border:none;")
        self.Selectjob.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/select.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Selectjob.setIcon(icon)
        self.Selectjob.setIconSize(QtCore.QSize(106, 106))
        self.Selectjob.setObjectName("Selectjob")
        self.Selectjob.clicked.connect(self.OpenFile)
        self.FinishPrint = QtWidgets.QPushButton(self.centralwidget)
        self.FinishPrint.setGeometry(QtCore.QRect(1, 360, 340, 240))
        self.FinishPrint.setStyleSheet("background-color: rgb(60, 181, 228); border:none;")
        self.FinishPrint.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/customer-support.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FinishPrint.setIcon(icon1)
        self.FinishPrint.setIconSize(QtCore.QSize(106, 106))
        self.FinishPrint.setObjectName("FinishPrint")
        self.StartPrint = QtWidgets.QPushButton(self.centralwidget)
        self.StartPrint.setGeometry(QtCore.QRect(342, 120, 340, 240))
        self.StartPrint.setStyleSheet("background-color: rgb(60, 181, 228); border:none;")
        self.StartPrint.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/play-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StartPrint.setIcon(icon2)
        self.StartPrint.setIconSize(QtCore.QSize(106, 106))
        self.StartPrint.setObjectName("StartPrint")
        self.StartPrint.clicked.connect(self.printstart)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(342, 360, 340, 240))
        self.pushButton_7.setStyleSheet("background-color: rgb(60, 181, 228); border:none;")
        self.pushButton_7.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon3)
        self.pushButton_7.setIconSize(QtCore.QSize(106, 106))
        self.pushButton_7.setObjectName("pushButton_7")
        self.closewin = QtWidgets.QPushButton(self.centralwidget)
        self.closewin.setGeometry(QtCore.QRect(964, 0, 61, 61))
        self.closewin.setAutoFillBackground(False)
        self.closewin.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/reverse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closewin.setIcon(icon4)
        self.closewin.setIconSize(QtCore.QSize(26, 26))
        self.closewin.setObjectName("closewin")
        self.closewin.clicked.connect(self.on_close)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 310, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(60, 181, 228);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(490, 310, 47, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(60, 181, 228);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(130, 550, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(60, 181, 228);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(490, 550, 47, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(60, 181, 228);")
        self.label_5.setObjectName("label_5")
        SecondWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def OpenFile(self): #to select the desired sliced file
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        #print(path)
        with zipfile.ZipFile(path, 'r') as zipobj:
            #print(zipobj.namelist())
            inflist = zipobj.namelist()
            zipobj.extractall()
            #print(inflist)
            for name in inflist:
                if name.endswith('.png'):
                    ifile = zipobj.open(name)
                    img = Image.open(ifile)
                    #print(img)
                elif name.endswith('.xml'): #To read the xml files from sliced (zip) folder
                    with open(name, 'r', encoding='utf-8') as fd:
                        print("pass")
                        result = xmltodict.parse(fd.read())
                        global printprofile
                        printprofile = result['PrintProfile']
                        #print (printprofile)
                        global ExposureTime
                        #print("Exposure Time:",ExposureTime)
                        break
        
    def printstart(self): #All the printing process /step by step
        mainmotor.vardeclare()
        print(mainmotor.delay)
        mainmotor.takefile()
        #ExposureTime = printprofile['ExposureTime']
        #print("Exposure Time:", ExposureTime)
        #time.sleep(5)
        #self.openWindow2()#Takes us to postcuring selection (Important for MDR project purpose)
        #self.StartPrint.clicked.connect(self.openWindow2)

    def on_close(self): #to close the Second window by clicking back button
        # win2 = QMainWindow()
        # ui = Ui_Win2()
        # ui.setupUi(win2)
        self.SecondWindow.close()

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "MainWindow"))
        self.label.setText(_translate("SecondWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt;\">Print</span></p></body></html>"))
        self.label_2.setText(_translate("SecondWindow", "Print Job"))
        self.label_3.setText(_translate("SecondWindow", "Start"))
        self.label_4.setText(_translate("SecondWindow", "Settings"))
        self.label_5.setText(_translate("SecondWindow", "Stop"))
import source_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SecondWindow = QtWidgets.QMainWindow()
    ui = Ui_SecondWindow()
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())

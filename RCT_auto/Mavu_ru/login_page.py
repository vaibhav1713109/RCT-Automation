from PyQt5 import QtWidgets, uic
import sys,os
from Downlink_Page2 import Ui_set_value__MainWindow
from popup import Ui_popup
dir_name = os.path.dirname(os.path.abspath(__file__))
#! /home/vvdn/Documents/Mavenir_8/Mavenir_8/bin/python

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('{}/Home_Page.ui'.format(dir_name), self)
        self.username = self.findChild(QtWidgets.QLineEdit, 'username')
        self.password = self.findChild(QtWidgets.QLineEdit, 'password')
        self.button = self.findChild(QtWidgets.QPushButton, 'login')
        self.button.clicked.connect(self.openWindow)
        self.show()

    def openWindow(self):
        li = []
        uss = self.username.text()
        pss = self.password.text()
        li.append(uss)
        li.append(pss)
        print(li)
        file1 = open("{}/myfile.ini".format(dir_name), "w")
        file1.writelines(f'{uss}\n')
        file1.writelines(pss)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_set_value__MainWindow()
        self.ui.setupUi(self.window)
        if uss == 'root':
            if pss == 'root':
                self.window.show()
                window.hide()
            else:
                self.window = QtWidgets.QMainWindow()
                self.ui = Ui_popup()
                self.ui.setupUi(self.window)
                self.window.show()
        else:
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_popup()
            self.ui.setupUi(self.window)
            self.window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application


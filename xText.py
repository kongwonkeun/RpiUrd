#
#
#
import os
import sys
import argparse
import subprocess
import time

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
#from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt
from PySide2.QtGui import QSurfaceFormat, QFont

#===============================
#
#
if __name__ == '__main__':

    app = QApplication(sys.argv)

    #win = QMainWindow()
    #win.setGeometry(100, 100, 800, 400)

    #win.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
    #win.setAttribute(Qt.WA_NoSystemBackground)
    #win.setAttribute(Qt.WA_TranslucentBackground)
    #win.setStyleSheet('background-color: rgba(128,0,0,128);')

    web = QWidget()
    web.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
    l = QLabel("---- T E X T ----", web)
    l.move(10, 10)
    l.setFont(QFont('궁서', 100))
    l.setStyleSheet('Color: green')
    web.setAttribute(Qt.WA_NoSystemBackground)
    web.setAttribute(Qt.WA_TranslucentBackground)
    #web.setStyleSheet('background-color: rgba(255,255,255,128);')
    web.setGeometry(0, 0, 800, 400)
    web.show()

    sys.exit(app.exec_())

#
#
#
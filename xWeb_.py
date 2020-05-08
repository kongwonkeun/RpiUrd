#
#
#
import os
import sys
import argparse
import subprocess
import time

from PySide2.QtWidgets import QApplication
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt

#===============================
#
#
if __name__ == '__main__':

    app = QApplication(sys.argv)
    web = QWebEngineView()

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('X', type=int, help='1st is x')
    parser.add_argument('Y', type=int, help='2nd is y')
    parser.add_argument('W', type=int, help='3rd is w')
    parser.add_argument('H', type=int, help='4th is h')
    parser.add_argument('U', type=str, help='5th is u')

    arg = parser.parse_args()
    left = arg.X
    top = arg.Y
    width = arg.W
    height = arg.H
    url = arg.U
    '''

    web.setWindowFlags(Qt.FramelessWindowHint)
    web.setGeometry(100, 100, 800, 400)
    web.setAttribute(Qt.WA_DeleteOnClose, False)
    web.setFocusPolicy(Qt.NoFocus)
    web.setContextMenuPolicy(Qt.NoContextMenu)
    web.setDisabled(True)
    web.load('http://www.google.com/')
    web.show()

    sys.exit(app.exec_())

#
#
#
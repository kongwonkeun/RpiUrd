#
#
#
import os
import sys
import argparse
import subprocess
import time

'''
from PySide2.QtWidgets import QApplication
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt
'''

#===============================
#
#
if __name__ == '__main__':

    c = subprocess.Popen(['unclutter','-display',':0','-idle','0','-noevents','-root'])
    #os.system('chromium-browser --kiosk http://www.google.com')
    #p = subprocess.Popen(['chromium-browser','--kiosk','http://www.google.com'])
    #p = subprocess.Popen(['chromium-browser','--kiosk','file:///home/pi/rdtone/tabata/index.html'])
    p = subprocess.Popen([
        'chromium-browser',
        '--window-size=800,600',
        '--window-position=100,100',
        '--disable-infobars',
        #'--kiosk',
        'file:///home/pi/rdtone/urd/content/3_5_4.html'
    ])
    time.sleep(10)
    p.kill()
    c.kill()
    sys.exit()

    '''
    app = QApplication(sys.argv)
    web = QWebEngineView()

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

    web.setWindowFlags(Qt.FramelessWindowHint)
    web.setGeometry(left, top, width, height)
    web.setAttribute(Qt.WA_DeleteOnClose, False)
    web.setFocusPolicy(Qt.NoFocus)
    web.setContextMenuPolicy(Qt.NoContextMenu)
    web.setDisabled(True)
    web.load(url)
    web.show()

    sys.exit(app.exec_())
    '''

#
#
#
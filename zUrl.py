#
#
#
import os
import sys
import signal
import socket

from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtCore import QTimer, Qt

#===============================
#
#
def handler():
    app.quit()

#================================
#
#
if  __name__ == '__main__':

    app = QApplication(sys.argv)
    win = app.desktop().screenGeometry()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('gmail.com', 80))
    ip = sock.getsockname()[0]
    print(f'IP={ip}')
    sock.close()

    signal.signal(signal.SIGINT, handler)

    tm = QTimer()
    tm.setSingleShot(True)
    tm.timeout.connect(handler)
    tm.start(10000)

    url = QLabel()
    url.setWindowFlags(Qt.FramelessWindowHint)
    url.setGeometry(win)
    url.setAttribute(Qt.WA_DeleteOnClose, False)
    url.setFocusPolicy(Qt.NoFocus)
    url.setContextMenuPolicy(Qt.NoContextMenu)
    url.setStyleSheet('background-color: black;')
    url.setText('<font size=10 color=white>http://%s:8080</font>' % ip)
    url.setAlignment(Qt.AlignCenter)
    url.show()

    sys.exit(app.exec_())

#
#
#
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

    l = QLabel()
    l.setWindowFlags(Qt.FramelessWindowHint)
    l.setGeometry(win)
    l.setAttribute(Qt.WA_DeleteOnClose, False)
    l.setFocusPolicy(Qt.NoFocus)
    l.setContextMenuPolicy(Qt.NoContextMenu)
    l.setStyleSheet('background-color: black; font: 72pt')
    l.setText(f'<font color=white>IP = {ip}</font>')
    l.setAlignment(Qt.AlignCenter)
    l.show()

    sys.exit(app.exec_())

#
#
#
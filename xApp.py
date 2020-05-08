#
#
#
import sys
import argparse
import signal
import time

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer

import yWin

#===============================
#
#
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('id', type=str, help='id is the layout id to show')
    parser.add_argument('time', type=int, help='time is the play time (sec) of layout')

    arg = parser.parse_args()
    id = arg.id
    time_ = arg.time

    app = QApplication(sys.argv)
    win = app.desktop().screenGeometry()

    signal.signal(signal.SIGINT, lambda s, f: app.quit())

    r = -1
    with yWin.Win(id, time_) as w:
        t = QTimer()
        t.setSingleShot(True)
        t.timeout.connect(w.showFullScreen)
        t.start(1000)
        w.setGeometry(win)
        w.show()
        r = app.exec_()

    sys.exit()

#
#
#
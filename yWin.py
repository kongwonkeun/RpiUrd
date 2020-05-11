#
#
#
import os
import sys
import signal
import time

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtCore import SIGNAL, Signal, Slot
from PySide2.QtCore import Qt, QThread, QTimer

import yLayout
import yRegion

#===============================
#
#
class Win(QMainWindow):

    def __init__(self, id, time):
        super(Win, self).__init__()
        self.regions = []
        self.running = False
        self.layout_id = id
        self.layout_time = time
        self.layout_timer = QTimer()
        self.layout_timer.setSingleShot(True)
        self.layout_timer.timeout.connect(self.stop)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        #---- kong ----
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        #----

    def __enter__(self):
        self.play(self.layout_id)
        self.layout_timer.setInterval(self.layout_time*1000)
        self.layout_timer.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if  exc_tb or exc_type or exc_val:
            pass

    def play(self, layout_id):
        path = f'content/{layout_id}.xml'
        layout = yLayout.get_layout(path)

        if  not layout:
            print('---- yWin: layout error ----')
            return False
        
        color = layout['bgcolor']
        self.setStyleSheet(f'background-color: {color}')
        
        #---- kong ----
        for region in layout['regions']:
            region['layout_id'] = layout_id
            r = yRegion.get_region(region, self.widget)
            self.regions.append(r)

        if  self.regions:
            for r in self.regions:
                r.play_end_signal.connect(self.replay)
                r.play()
        #----
        return True

    @Slot()
    def replay(self):
        print('---- yWin: replay ----')
        if  self.regions:
            for r in self.regions:
                r.play()

    def stop(self):
        if  self.regions:
            for r in self.regions:
                r.stop()

        self.regions = []  #---- del self.regions[:]
        self.widget = None
        #self.widget = QWidget()
        #self.setCentralWidget(self.widget)
        print(f'---- yWin: stop to close ----')
        #---- kong ----
        self.close()
        #----

#================================
#
#
if  __name__ == '__main__':

    app = QApplication(sys.argv)
    win = app.desktop().screenGeometry()

    signal.signal(signal.SIGINT, lambda s, f: app.quit())

    r = -1
    with Win('2', 10) as w:
        t = QTimer()
        t.setSingleShot(True)
        t.timeout.connect(w.showFullScreen)
        t.start(1000)
        w.setGeometry(win)
        w.show()
        r = app.exec_()

    sys.exit(r)

#
#
#
#
#
#
import os
import sys
import signal
import time

from PySide2.QtCore import QObject, QProcess, QTimer
from PySide2.QtCore import SIGNAL, Signal, Slot
from PySide2.QtCore import QUrl, QByteArray
from PySide2.QtCore import QRect
from PySide2.QtCore import Qt
from PySide2 import QtPrintSupport
from PySide2.QtGui import QImage, QPixmap, QPixmapCache
from PySide2.QtWidgets import QWidget, QLabel
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent

#================================
#
#
class Media(QObject):

    started_signal = Signal()
    finished_signal = Signal()

    def __init__(self, media, parent_widget):
        super(Media, self).__init__(parent_widget)
        self.parent_widget = parent_widget
        self.id = media['id']
        self.type = media['type']
        self.duration = media['duration']
        self.render = media['render']
        self.options = media['options']
        self.raws = media['raws']

        self.layout_id = media['layout_id']
        self.region_id = media['region_id']
        self.zindex = media['zindex']
        self.widget = None
        self.play_timer = QTimer(self)
        self.started = 0
        self.finished = 0
        self.errors = None
        self.connect_signals()

    def connect_signals(self):
        self.started_signal.connect(self.mark_started)
        self.finished_signal.connect(self.mark_finished)
        self.play_timer.setSingleShot(True)
        self.connect(self.play_timer, SIGNAL('timeout()'), self.stop)

    @Slot()
    def play(self):
        pass

    @Slot()
    def stop(self, delete_widget=False):
        if  self.is_finished():
            return False
        if  self.widget:
            tries = 10
            while tries > 0 and not self.widget.close():
                tries -= 1
                time.msleep(100)
            if  delete_widget:
                del self.widget  #---- ? ----
                self.widget = None
        self.finished_signal.emit()
        return True

    @Slot()
    def mark_started(self):
        self.started = time.time()

    @Slot()
    def mark_finished(self):
        if  not self.is_finished():
            self.finished = time.time()

    def is_started(self):
        return self.started > 0

    def is_finished(self):
        return self.finished > 0

    def is_playing(self):
        return self.is_started() and not self.is_finished()

    def set_default_widget_prop(self):
        if  self.widget is not None:
            self.widget.setAttribute(Qt.WA_DeleteOnClose, False)
            self.widget.setFocusPolicy(Qt.NoFocus)
            self.widget.setContextMenuPolicy(Qt.NoContextMenu)
            self.widget.setObjectName('%s-widget' % self.objectName())
            #---- kong ----
            self.widget.setAttribute(Qt.WA_TranslucentBackground)
            self.widget.setWindowFlags(Qt.FramelessWindowHint)
            #----

#================================
#
#
class MediaImage(Media):

    def __init__(self, media, parent_widget):
        super(MediaImage, self).__init__(media, parent_widget)
        self.widget = QLabel(parent_widget)
        self.widget.setGeometry(media['geometry'])
        self.img = QImage()
        self.set_default_widget_prop()

    @Slot()
    def play(self):
        self.finished = 0
        uri = self.options['uri']
        path = f'content/{uri}'
        rect = self.widget.geometry()
        self.img.load(path)
        self.img = self.img.scaled(
            rect.width(),
            rect.height(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        self.widget.setPixmap(QPixmap.fromImage(self.img))
        self.widget.show()
        self.widget.raise_()
        if  float(self.duration) > 0:
            self.play_timer.setInterval(int(float(self.duration) * 1000))
            self.play_timer.start()
        self.started_signal.emit()

    @Slot()
    def stop(self, delete_widget=False):
        #---- kong ----
        if  not self.widget:
            return False
        del self.img
        self.img = QImage()
        #----
        super(MediaImage, self).stop(delete_widget)
        return True

#===============================
#
#
class MediaVideo(Media):

    def __init__(self, media, parent_widget):
        super(MediaVideo, self).__init__(media, parent_widget)
        self.widget = QWidget(parent_widget)
        self.process = QProcess(self.widget)
        self.process.setObjectName('%s-process' % self.objectName())
        self.std_out = []
        self.errors = []
        self.stopping = False
        self.mute = False
        self.widget.setGeometry(media['geometry'])
        self.connect(self.process, SIGNAL('error()'), self.process_error)
        self.connect(self.process, SIGNAL('finished()'), self.process_finished)
        self.connect(self.process, SIGNAL('started()'), self.process_started)
        self.set_default_widget_prop()
        self.stop_timer = QTimer(self)
        self.stop_timer.setSingleShot(True)
        self.stop_timer.setInterval(1000)
        self.stop_timer.timeout.connect(self.process_timeout)
        #---- kong ---- for RPi
        self.rect = media['geometry']
        #----

    @Slot()
    def process_timeout(self):
        os.kill(self.process.pid(), signal.SIGTERM)
        self.stopping = False
        if  not self.is_started():
            self.started_signal.emit()
        super(MediaVideo, self).stop()

    @Slot(object)
    def process_error(self, err):
        print('---- process error ----')
        self.errors.append(err)
        self.stop()

    @Slot()
    def process_finished(self):
        self.stop()

    @Slot()
    def process_started(self):
        self.stop_timer.stop()
        if  float(self.duration) > 0:
            self.play_timer.setInterval(int(float(self.duration) * 1000))
            self.play_timer.start()
        self.started_signal.emit()
        pass

    @Slot()
    def play(self):
        self.finished = 0
        self.widget.show()
        self.widget.raise_()
        uri = self.options['uri']
        path = f'content/{uri}'
        #---- kong ---- for RPi
        left, top, right, bottom = self.rect.getCoords()
        rect = f'{left},{top},{right},{bottom}'
        args = [ '--win', rect, '--no-osd', '--layer', self.zindex, path ]
        self.process.start('omxplayer.bin', args)
        self.stop_timer.start()
        #----

    @Slot()
    def stop(self, delete_widget=False):
        #---- kong ---- for RPi
        if  not self.widget:
            return False
        if  self.stopping or self.is_finished():
            return False
        self.stop_timer.start()
        self.stopping = True
        if  self.process.state() == QProcess.ProcessState.Running:
            self.process.write(b'q')
            self.process.waitForFinished()
            self.process.close()
        super(MediaVideo, self).stop(delete_widget)
        self.stopping = False
        self.stop_timer.stop()
        return True
        #----

#===============================
#
#
class MediaWeb(Media):

    def __init__(self, media, parent_widget):
        super(MediaWeb, self).__init__(media, parent_widget)
        self.widget = QWidget(parent_widget)
        self.process = QProcess(self.widget)
        self.process.setObjectName('%s-process' % self.objectName())
        self.std_out = []
        self.errors = []
        self.stopping = False
        self.mute = False
        self.widget.setGeometry(media['geometry'])
        self.connect(self.process, SIGNAL('error()'), self.process_error)
        self.connect(self.process, SIGNAL('finished()'), self.process_finished)
        self.connect(self.process, SIGNAL('started()'), self.process_started)
        self.set_default_widget_prop()
        self.stop_timer = QTimer(self)
        self.stop_timer.setSingleShot(True)
        self.stop_timer.setInterval(1000)
        self.stop_timer.timeout.connect(self.process_timeout)
        self.rect = self.widget.geometry()

    @Slot()
    def process_timeout(self):
        os.kill(self.process.pid(), signal.SIGTERM)
        self.stopping = False
        if  not self.is_started():
            self.started_signal.emit()
        super(MediaWeb, self).stop()

    @Slot(object)
    def process_error(self, err):
        print('---- process error ----')
        self.errors.append(err)
        self.stop()

    @Slot()
    def process_finished(self):
        self.stop()

    @Slot()
    def process_started(self):
        self.stop_timer.stop()
        if  float(self.duration) > 0:
            self.play_timer.setInterval(int(float(self.duration) * 1000))
            self.play_timer.start()
        self.started_signal.emit()
        pass

    @Slot()
    def play(self):
        self.finished = 0
        self.widget.show()
        self.widget.raise_()
        #---- kong ----
        url = self.options['uri']
        l = str(self.rect.left())
        t = str(self.rect.top())
        w = str(self.rect.width())
        h = str(self.rect.height())
        s = f'--window-size={w},{h}'
        p = f'--window-position={l},{t}'
        args = [
            '--kiosk', s, p, QUrl.fromPercentEncoding(QByteArray(url.encode('utf-8')))
            #l, t, w, h, QUrl.fromPercentEncoding(QByteArray(url.encode('utf-8')))
        ]
        self.process.start('chromium-browser', args)
        #self.process.start('./xWeb', args)
        self.stop_timer.start()
        #----

    @Slot()
    def stop(self, delete_widget=False):
        #---- kong ----
        if  not self.widget:
            return False
        if  self.stopping or self.is_finished():
            return False
        self.stop_timer.start()
        self.stopping = True
        if  self.process.state() == QProcess.ProcessState.Running:
            #---- kill process ----
            os.system('pkill chromium')
            #os.system('pkill xWeb')
            #----
            self.process.waitForFinished()
            self.process.close()
        super(MediaWeb, self).stop(delete_widget)
        self.stopping = False
        self.stop_timer.stop()
        return True
        #----

#================================
#
#
class MediaText(Media):

    def __init__(self, media, parent_widget):
        super(MediaText, self).__init__(media, parent_widget)
        self.widget = QWidget(parent_widget)
        self.process = QProcess(self.widget)
        self.process.setObjectName('%s-process' % self.objectName())
        self.std_out = []
        self.errors = []
        self.stopping = False
        self.mute = False
        self.widget.setGeometry(media['geometry'])
        self.connect(self.process, SIGNAL('error()'), self.process_error)
        self.connect(self.process, SIGNAL('finished()'), self.process_finished)
        self.connect(self.process, SIGNAL('started()'), self.process_started)
        self.set_default_widget_prop()
        self.stop_timer = QTimer(self)
        self.stop_timer.setSingleShot(True)
        self.stop_timer.setInterval(1000)
        self.stop_timer.timeout.connect(self.process_timeout)
        self.rect = self.widget.geometry()

    @Slot()
    def process_timeout(self):
        os.kill(self.process.pid(), signal.SIGTERM)
        self.stopping = False
        if  not self.is_started():
            self.started_signal.emit()
        super(MediaText, self).stop()

    @Slot(object)
    def process_error(self, err):
        print('---- process error ----')
        self.errors.append(err)
        self.stop()

    @Slot()
    def process_finished(self):
        self.stop()

    @Slot()
    def process_started(self):
        self.stop_timer.stop()
        if  float(self.duration) > 0:
            self.play_timer.setInterval(int(float(self.duration) * 1000))
            self.play_timer.start()
        self.started_signal.emit()
        pass

    @Slot()
    def play(self):
        self.finished = 0
        self.widget.show()
        self.widget.raise_()
        #---- kong ----
        path = f'file:///home/pi/rdtone/urd/content/{self.layout_id}_{self.region_id}_{self.id}.html'
        
        print(path)
        
        l = str(self.rect.left())
        t = str(self.rect.top())
        w = str(self.rect.width())
        h = str(self.rect.height())
        s = f'--window-size={w},{h}'
        p = f'--window-position={l},{t}'
        args = [
            '--kiosk', s, p, path
            #l, t, w, h, path
        ]
        self.process.start('chromium-browser', args)
        #self.process.start('./xWeb', args)
        self.stop_timer.start()
        #----

    @Slot()
    def stop(self, delete_widget=False):
        #---- kong ----
        if  not self.widget:
            return False
        if  self.stopping or self.is_finished():
            return False
        self.stop_timer.start()
        self.stopping = True
        if  self.process.state() == QProcess.ProcessState.Running:
            #---- kill process ----
            os.system('pkill chromium')
            #os.system('pkill xWeb')
            #----
            self.process.waitForFinished()
            self.process.close()
        super(MediaText, self).stop(delete_widget)
        self.stopping = False
        self.stop_timer.stop()
        return True
        #----

#================================
#
#
'''
class MediaText_(Media):

    def __init__(self, media, parent_widget):
        super(MediaText_, self).__init__(media, parent_widget)
        self.widget = QWebEngineView(parent_widget)
        self.widget.setGeometry(media['geometry'])
        self.set_default_widget_prop()
        self.widget.setDisabled(True)

    @Slot()
    def play(self):
        self.finished = 0
        path = '%s/%s_%s_%s.html' % (
            self.save_dir,
            self.layout_id,
            self.region_id,
            self.id
        )
        self.widget.load('file:///' + path)
        self.widget.show()
        self.widget.raise_()
        if  float(self.duration) > 0:
            self.play_timer.setInterval(int(float(self.duration) * 1000))
            self.play_timer.start()
        self.started_signal.emit()

    @Slot()
    def stop(self, delete_widget=False):
        #---- kong ----
        if  not self.widget:
            return False
        super(MediaText_, self).stop(delete_widget)
        return True
        #----
'''

#================================
#
#
def get_media(media, parent_widget):

    print(f'---- yMedia: get ----')
    if  'type' not in media:
        return None

    if  'image' == media['type']:
        media_ = MediaImage(media, parent_widget)
    elif 'video' == media['type']:
        media_ = MediaVideo(media, parent_widget)
    elif 'webpage' == media['type']:
        media_ = MediaWeb(media, parent_widget)
    else:
        media_ = MediaText(media, parent_widget)

    return media_

#================================
#
#
if  __name__ == '__main__':

    sys.exit()

#
#
#
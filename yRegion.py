#
#
#
import sys
import signal

from PySide2.QtCore import QObject, QRect
from PySide2.QtCore import SIGNAL, Signal, Slot

import yMedia

#===============================
#
#
class Region(QObject):

    play_end_signal = Signal()

    def __init__(self, region, parent_widget):
        super(Region, self).__init__(parent_widget)
        self.parent_widget = parent_widget
        self.id = region['id']
        self.width = region['width']
        self.height = region['height']
        self.left = region['left']
        self.top = region['top']
        self.zindex = region['zindex']
        self.media = region['media']

        self.loop = False
        self.layout_id = region['layout_id']
        self.media_list = []
        self.media_index = 0
        self.media_length = 0
        self.stop_ = False
        self.populate_media()
        self.play_end_signal.connect(self.sig)

    @Slot()
    def sig(self):
        # temporal signal
        pass

    def populate_media(self):
        print(f'---- yRegion: populate ----')
        for medium in self.media:
            medium['layout_id'] = self.layout_id
            medium['region_id'] = self.id
            medium['zindex'] = self.zindex
            medium['geometry'] = QRect(
                int(float(self.left)),
                int(float(self.top)),
                int(float(self.width)),
                int(float(self.height))
            )
            m = yMedia.get_media(medium, self.parent_widget)
            if  m is not None:
                m.finished_signal.connect(self.play_next)
                self.media_list.append(m)
                self.media_length += 1

    def play(self):
        if  self.stop_ or self.media_length < 1:
            return None
        
        print(f'---- yRegion: play ----')
        self.media_list[self.media_index].play()

    def play_next(self):
        self.media_index += 1
        if  self.loop:
            if  self.media_index >= self.media_length:
                self.media_index = 0
        if  self.media_index < self.media_length:
            self.play()
        else:
            self.media_index = 0
            self.play_end_signal.emit()

    def stop(self):
        self.stop_ = True
        for m in self.media_list:
            if  m.is_playing():
                m.stop(delete_widget=True)

        self.media_list = []  #---- del self.medias[:]

#================================
#
#
def get_region(region, parent_widget):

    print(f'---- yRegion: get ----')
    region_ = Region(region, parent_widget)
    return region_

#================================
#
#
if  __name__ == '__main__':

    sys.exit()

#
#
#
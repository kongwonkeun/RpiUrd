#
#
#
import sys
from xml.etree import ElementTree

#================================
#
#
class Layout:

    def __init__(self, path=None):
        self.layout = None
        if  path:
            self.layout = self.parse_layout(path)

    #============================
    #
    #
    def parse_layout(self, path):

        layout = {
            'width': '',
            'height': '',
            'bgcolor': '',
            'background': '',
            'regions': []
        }
        tree = ElementTree.parse(path)
        root = tree.getroot()

        if  'layout' != root.tag:
            self.layout = None
            return None
        
        for k, v in root.attrib.items():
            if  k in layout:
                layout[k] = v

        for child in root:
            if  'region' == child.tag:
                region = self.parse_region(child)
                if  region:
                    layout['regions'].append(region)
        return layout

    #============================
    #
    #
    def parse_region(self, node):

        if  node is None:
            return None

        region = {
            'id': '',
            'width': '',
            'height': '',
            'left': '',
            'top': '',
            'userId': '',
            'zindex': '0',
            'media': []
        }

        for k, v in node.attrib.items():
            if  k in region:
                region[k] = v

        for child in node:
            if  'media' == child.tag:
                media = self.parse_media(child)
                if  media:
                    region['media'].append(media)
        return region

    #============================
    #
    #
    def parse_media(self, node):
        
        if  node is None:
            return None
        
        media = {
            'id': '',
            'type': '',
            'duration': '',
            'render': '',
            'options': {},
            'raws': {}
        }

        for k, v in node.attrib.items():
            if  k in media:
                media[k] = v
        
        for child in node:
            if  'options' == child.tag:
                for option in child:
                    if  option.text:
                        media['options'][option.tag] = option.text
            elif 'raw' == child.tag:
                for raw in child:
                    if  raw.text:
                        media['raws'][raw.tag] = raw.text
        return media

#================================
#
#
def get_layout(path):

    layout = None

    try:
        l = Layout(path)
    except ElementTree.ParseError:
        print(f'---- yLayout: parse error ----')
        return layout
    except IOError:
        print(f'---- yLayout: io error ----')
        return layout
    
    if  l.layout:
        layout = dict(l.layout)
        l = None

    return layout

#================================
#
#
if  __name__ == '__main__':

    path = 'content/1.xml'
    layout = get_layout(path)
    print(layout)
    sys.exit()

#
#
#
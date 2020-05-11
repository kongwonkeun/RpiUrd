#
#
#
import os
import sys
import argparse
import subprocess
import time

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

#
#
#
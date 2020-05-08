#
#
#
import os
import sys
import threading
import time
import errno

#================================
#
#
PIPE_FOO = 'foo'
PIPE_FOOBAR = 'foobar'
PIPE_BUF_SIZE = 65536

SHOW_ON = 'on'
SHOW_OFF = 'off'

G_server = { PIPE_FOO: None, PIPE_FOOBAR: None }

#================================
#
#
class Pipe:

    def __init__(self):
        pass

#================================
#
#
class PipeServer(Pipe):

    def __init__(self, callback=None):
        self.callback = callback
        self.count = 0
        self.q = False
        self.launcher()
    
    def launcher(self):
        threading.Thread(target=self.server, args=(), daemon=True).start()
        threading.Thread(target=self.server, args=(PIPE_FOOBAR,), daemon=True).start()

    def quit(self):
        self.q = True

    #============================
    #
    #
    def server(self, pipe=PIPE_FOO):
        global G_server
        print(f'{pipe} server begin')

        try:
            os.mkfifo(pipe)
        except OSError as e:
            if  e.errno != errno.EEXIST:
                raise

        while not self.q:
            if  G_server[pipe] == None:
                p = os.open(pipe, os.O_WRONLY) #---- blocking ----
                G_server[pipe] = p

                try:
                    while not self.q:
                        self.count += 1
                        d = str.encode(f'{self.count}') # encode to byte stream
                        os.write(p, d) # send
                        time.sleep(1)

                except BrokenPipeError:
                    pass

                os.close(p)
                G_server[pipe] = None
            time.sleep(1)

        print(f'{pipe} server end')
        os.remove(pipe)

#================================
#
#
class PipeClient(Pipe):

    def __init__(self, pipe=PIPE_FOO, show=SHOW_ON, callback=None):
        self.pipe = pipe
        self.show = show
        self.callback = callback
        self.count = 0
        self.q = False
        threading.Thread(target=self.client, args=()).start()
    
    def quit(self):
        self.q = True

    #============================
    #
    #
    def client(self):
        print(f'{self.pipe} client begin')

        while not self.q:
            p = os.open(self.pipe, os.O_RDONLY)

            while not self.q:
                d = os.read(p, PIPE_BUF_SIZE) #---- blocking ----
                if  len(d) == 0:
                    break

                if  self.show == SHOW_ON:
                    print(f'receive {d.decode()}') # decide to string
                if  self.callback != None:
                    self.callback(d.decode())

            os.close(p)
        print(f'{self.pipe} client end')

#================================
#
#
if  __name__ == '__main__':

    '''
    client = PipeClient()
    input('press any key to exit ...')
    client.quit()
    '''

    server = PipeServer()
    input('press any key to exit ...')
    server.quit()
    sys.exit()

#
#
#
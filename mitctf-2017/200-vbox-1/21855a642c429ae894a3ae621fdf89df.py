#!/usr/bin/python

import socket
import thread


class MachineSocket:
    socket = None
    active = thread.allocate_lock()

    def __init__(self, machine):
        self.machine = machine

    def do_read(self, dest, ln):
        data = self.sread(ln)
        if data:
            for i in range(ln):
                c = 0
                if i < len(data):
                    c = ord(data[i])
                self.machine.mset(dest + i, c)
        self.active.release()

    def do_write(self, src, ln):
        data = ''
        for i in range(ln):
            data += chr(self.machine.mget(src + i) % 256)
        self.swrite(data)
        self.sflush()
        self.active.release()

    def do_close(self):
        try:
            self.socket.close()
        except:
            pass

    def read(self, dest, ln):
        self.active.acquire()
        thread.start_new_thread(self.do_read, (dest, ln))

    def write(self, src, ln):
        self.active.acquire()
        thread.start_new_thread(self.do_write, (src, ln))

    def seek(self, offset):
        self.active.acquire()
        self.sseek(offset)
        self.active.release()

    def tell(self):
        self.active.acquire()
        ret = self.stell()
        self.active.release()
        return ret

    def close(self):
        self.do_close()

    def wait(self):
        self.active.acquire()
        self.active.release()


class StdSocket(MachineSocket):
    def __init__(self, machine, socket):
        MachineSocket.__init__(self, machine)
        self.socket = socket
        self.sread = self.socket.read
        self.swrite = self.socket.write
        self.sflush = self.socket.flush
        self.sseek = lambda: None
        self.stell = lambda: None


class NetworkSocket(MachineSocket):
    def __init__(self, machine, address, port):
        MachineSocket.__init__(self, machine)
        self.socket = socket.socket()
        try:
            self.socket.connect((address, port))
            self.sread = self.socket.recv
            self.swrite = self.socket.send
        except:
            self.sread = lambda _: None
            self.swrite = lambda _: None
        self.sflush = lambda: None
        self.sseek = lambda: None
        self.stell = lambda: None

listeners = {}
class ListenerSocket(MachineSocket):

    def __init__(self, machine, port, reuse):
        MachineSocket.__init__(self, machine)
        if port in listeners and not reuse:
            listeners[port].close()
            del listeners[port]
        if port not in listeners:
            listeners[port] = socket.socket()
            listeners[port].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listeners[port].bind(('0.0.0.0', port))
            listeners[port].listen(2)

        try:
            self.socket = listeners[port].accept()[0]
            self.sread = self.socket.recv
            self.swrite = self.socket.send
        except:
            self.sread = lambda _: None
            self.swrite = lambda _: None

        self.sflush = lambda: None
        self.sseek = lambda: None
        self.stell = lambda: None


class FileSocket(MachineSocket):
    def __init__(self, machine, filename, flags):
        MachineSocket.__init__(self, machine)
        flag_string = ''
        if flags & 1: flag_string += 'r'
        if flags & 2: flag_string += 'w'
        if flags & 4: flag_string += 'a'
        self.socket = open(filename.strip(), flag_string)
        self.sread = self.socket.read
        self.swrite = self.socket.write
        self.sflush = self.socket.flush
        self.sseek = self.socket.seek
        self.stell = self.socket.tell

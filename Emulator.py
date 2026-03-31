
import posix_ipc
import mmap
import struct
from Policy import Policy

class Emulator:

    def __init__(self):

        self.shm = posix_ipc.SharedMemory("/RAM_MAP")
        self.py_flag = posix_ipc.Semaphore("/py_to_lua")
        self.lua_flag = posix_ipc.Semaphore("/lua_to_py")
        self.buffer = mmap.mmap(self.shm.fd,4104)
        self.shm.close_fd()

    def _policy(self):

        nn = Policy()
        

        return 0
    
    def read(self):
        
        self.lua_flag.acquire()
        state,size = struct.unpack('II',self.buffer[:8])
        info = self.buffer[8:8+4096].split(b'\x00',1)[0]

        xcoord,ycoord = info.decode().split(',')
        self.py_flag.release()
        return [xcoord,ycoord]
    
    def input(self):

        actions = {0 : 'Up',1 : "Left", 2 : "Down",3 : "Right",4 : "A",5 : "B",6 : "Select",7 : "Start"}
        currX,currY = self.read()
        




        






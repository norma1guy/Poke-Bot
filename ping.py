import posix_ipc
import mmap
import struct

shm = posix_ipc.SharedMemory("/RAM_MAP")
lua = posix_ipc.Semaphore("/py_to_lua")
py  = posix_ipc.Semaphore("/lua_to_py")
mm = mmap.mmap(shm.fd, 4104)
shm.close_fd()

while True :
    py.acquire()
    

    state, size = struct.unpack("II", mm[:8])
    buffer = mm[8:8+4096].split(b"\x00", 1)[0]

    print(state, size, buffer.decode())

    '''message = b"hello lua"
    mm[8:8+len(message)] = message
    mm[8+len(message)] = 0
    mm[4:8] = struct.pack("I", len(message)) '''
    lua.release()
import posix_ipc
import mmap
import struct
from Memory import Memory


class Environment :

    def __init__(self,shm):
        self.ewram = Memory(shm)

    
    def get_coords(self):

        playerAvatar = 0x37590
        objectEvents = 0x37350
        objectSize = 0x24
        playerEvent = self.ewram.read_u8(playerAvatar + 5)
        playerObject = objectEvents + playerEvent * objectSize
        xCoord = self.ewram.read_s16_le(playerObject + 0x10)
        yCoord = self.ewram.read_s16_le(playerObject + 0x12)

        return [xCoord,yCoord]
    
    def get_party(self):
        






    

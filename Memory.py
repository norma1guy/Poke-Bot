import struct

class Memory :
    '''
    Allows access of binary memory data from the ram map
    '''
    def __init__(self,shm):
        self.ewram = shm[8:]

    def read_flag(self,offset):
        return struct.unpack_from('?', self.ewram, offset)[0]

    def read_u8(self,offset):
        return self.ewram[offset]
    
    def read_s8(self, offset):
        return struct.unpack_from('b', self.ewram, offset)[0]
    
    def read_s16_le(self,offset):
        return struct.unpack_from('<h',self.ewram,offset)[0] 
    
    def read_s16_be(self,offset):
        return struct.unpack_from('>h',self.ewram,offset)[0]
    
    def read_u16_le(self,offset):
        return struct.unpack_from('<H',self.ewram,offset)[0]
    
    def read_u16_be(self,offset):
        return struct.unpack_from('>H',self.ewram,offset)[0]

    def read_s32_le(self,offset):
        return struct.unpack_from('<i',self.ewram,offset)[0]
    
    def read_s32_be(self,offset):
        return struct.unpack_from('>i',self.ewram,offset)[0]
    
    def read_u32_le(self,offset):
        return struct.unpack_from('<I',self.ewram,offset)[0]
    
    def read_u32_be(self,offset):
        return struct.unpack_from('>I',self.ewram,offset)[0]
import struct

class Memory :
    '''
    Allows access of binary memory data from the ram map
    '''
    def __init__(self,shm):
        self.ram = shm

    def read_flag(self,offset):
        return struct.unpack_from('?', self.ram, offset)[0]

    def read_u8(self,offset):
        return self.ram[offset]
    
    def read_s8(self, offset):
        return struct.unpack_from('b', self.ram, offset)[0]
    
    def read_s16_le(self,offset):
        return struct.unpack_from('<h',self.ram,offset)[0] 
    
    def read_s16_be(self,offset):
        return struct.unpack_from('>h',self.ram,offset)[0]
    
    def read_u16_le(self,offset):
        return struct.unpack_from('<H',self.ram,offset)[0]
    
    def read_u16_be(self,offset):
        return struct.unpack_from('>H',self.ram,offset)[0]

    def read_s32_le(self,offset):
        return struct.unpack_from('<i',self.ram,offset)[0]
    
    def read_s32_be(self,offset):
        return struct.unpack_from('>i',self.ram,offset)[0]
    
    def read_u32_le(self,offset):
        return struct.unpack_from('<I',self.ram,offset)[0]
    
    def read_u32_be(self,offset):
        return struct.unpack_from('>I',self.ram,offset)[0]
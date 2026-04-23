import posix_ipc
import mmap
import struct
from Memory import Memory
from Map import Map




class Environment :

    def __init__(self):
        self.shm = posix_ipc.SharedMemory("/RAM_MAP")
        self.pyFlag = posix_ipc.Semaphore("/py_to_lua")
        self.luaFlag  = posix_ipc.Semaphore("/lua_to_py")
        self.ewramSize = 256 * 1024
        self.iwramSize = 32 * 1024
        self.mm = mmap.mmap(self.shm.fd,8 + self.ewramSize + self.iwramSize)
        self.shm.close_fd()
        self.input = struct.unpack("I",self.mm[:4])
        self.ewram = Memory(self.mm[8:8 + self.ewramSize])
        self.iwram = Memory(self.mm[8 + self.ewramSize : 8 + self.ewramSize + self.iwramSize])
        self.is_battle = False
        self.max_battlers = 4
        self.double_battle = False
        self.map = Map().build_graph()
        self.prevState = None
        self.input = {'A' : 0,'B' : 1,'Up' : 2,'Down' : 3, 'Left' : 4,'Right' : 5,'Select' : 6,'Start' : 7}


    def reset(self):
        mapState = self.get_coords()
        badges = self.get_badges()
        party = self.get_party()
        #battleState = self.get_battle_info()
        #hms = self.get_hms()

        state = {'map' : mapState,
                'badge' : badges,
                'party' : party,
                #'battle' : battleState,
                #'hms' : hms
                }
        
        return mapState

    
    def take_action(self,action):
        #print(69)
        print(self.luaFlag.value)
        self.luaFlag.acquire()
        #print(action)
        self.mm[:4] = struct.pack("I", action)
        nextState = self.reset()
        return nextState
    
    def calc_reward(self,nextState) :
        reward = 0
        '''# Badge reward
        if sum(next['badges']) > sum(prev['badges']) :
            reward += 10 
        
        # Movement reward
        if next['map'] != prev['map'] :
            reward += 0.1

        # HMs reward 
        if sum(next['hms']) > sum(prev['hms']) :
            reward += 10'''
        
        if not self.prevState :
            reward += 0.1
        elif sum(self.prevState) != sum(nextState) :
            reward += 0.1
        
        return reward
    
    def step(self,action) :
        nextState = self.take_action(action)
        reward = self.calc_reward(nextState)
        self.prevState = nextState
        self.pyFlag.release()

        return [nextState,reward,False]
    
    def get_hms(self) :
        hms = [0] * 8
        saveBlockAddr = self.iwram.read_u32_le(0x5d8c) # Using saveBlockPtr from IWRAM
        #print(saveBlockAddr)
        TMHMBagPocket = saveBlockAddr + 0x690
        for i in range(8) :
            hms[i] = 1 if self.ewram.read_u16_le(TMHMBagPocket + 339 + 4 * i) else 0

        return hms

   
    def get_coords(self):

        playerAvatar = 0x37590
        objectEvents = 0x37350
        objectSize = 0x24
        playerEvent = self.ewram.read_u8(playerAvatar + 5)
        playerObject = objectEvents + playerEvent * objectSize
        xCoord = self.ewram.read_s16_le(playerObject + 0x10)
        yCoord = self.ewram.read_s16_le(playerObject + 0x12)
        insideBuilding = 0
        pos = [xCoord,yCoord,insideBuilding]
        pos.extend(self.map)
        return pos
    
    def get_party(self):

        partyCount = self.ewram.read_u8(0x244e9)
        party = {}
        partyAddr = 0x244ec
        structSize = 104 # size of each Pokemon struct

        for i in range(partyCount):
            pokemon = partyAddr + i * structSize
            status = self.ewram.read_u32_le(pokemon + 0x50)
            level = self.ewram.read_u8(pokemon + 0x54)
            hp = self.ewram.read_u16_le(pokemon + 0x56)
            maxhp = self.ewram.read_u16_le(pokemon + 0x58)
            attack = self.ewram.read_u16_le(pokemon + 0x5a)
            defense = self.ewram.read_u16_le(pokemon + 0x5c)
            speed = self.ewram.read_u16_le(pokemon + 0x5e)
            spatt = self.ewram.read_u16_le(pokemon + 0x60)
            spdef = self.ewram.read_u16_le(pokemon + 0x62)
            party.update(
                { i :
                    {
                    'status' : status,
                    'level' : level,
                    'hp' : hp,
                    'maxhp' : maxhp,
                    'attack' : attack,
                    'defense' : defense,
                    'speed' : speed,
                    'spatt' : spatt,
                    'spdef' : spdef
                    }
                }
            )

        return party
    
    def get_badges(self):
        badges = [0] * 8
        gym_flag = 0x867
        for i in range(8) :
            badges[i] = 1 if self.ewram.read_flag(gym_flag) else 0
            gym_flag += 1

        return badges
    
    def get_battle_info(self):
        gBattleMons = 0x24084 # Max can have 4 BattlePokemon(88 bytes each)
        sizeBattlePokemon = 88
        #gEnemyPartyCount = self.ewram.read_u8(0x244ea)
        #gPlayerPartyCount = self.ewram.read_u8(0x244e9)
        #gCurrentMove = self.ewram.read_u16(0x0241ea)
        #gBattlerAttacker = self.ewram.read_u8(0x2420b)
        #gBattlerTarget = self.ewram.read_u8(0x2420c)
        #gLastMoves = [self.ewram.read_u16(hex(0x24248 + i * 2)) for i in range(4)]
        playerMon = []
        enemyMon = []
        finishBattle = 0
        for i in range(self.max_battlers) :
            mon = gBattleMons + i * sizeBattlePokemon
            attack = self.ewram.read_u16_le(mon + 0x2)
            if not attack :
                break
            elif attack and i > 1 :
                self.double_battle = True
            defense = self.ewram.read_u16_le(mon + 0x4)
            speed = self.ewram.read_u16_le(mon + 0x6)
            spAttack = self.ewram.read_u16_le(mon + 0x8)
            spDefense = self.ewram.read_u16_le(mon + 0xa)
            types = [self.ewram.read_u8(mon + 0x21),self.ewram.read_u8(hex(mon + 0x22))]
            pp = [self.ewram.read_u8(mon + 0x24 + i) for i in range(4)]
            statChanges = self.ewram.read_s8(mon + 0x18)
            status1 = self.ewram.read_u32_le(mon + 0x4C)
            status2 = self.ewram.read_u32_le(mon + 0x50)
            lvl = self.ewram.read_u8(mon + 0x2A)
            exp = self.ewram.read_u32_le(mon + 0x44)
            maxHP = self.ewram.read_u16_le(mon + 0x2C)
            hp = self.ewram.read_u16_le(mon + 0x28)
            ability = self.ewram.read_u8(mon + 0x20)
            moves = [self.ewram.read_u16_le(mon + 0x0C + 2 * i) for i in range(4)]
            holdItem = self.ewram.read_u16_le(mon + 0x2E)
            species = self.ewram.read_u16_le(mon)
            poke = {
                    'species' : species,
                    'att': attack,
                    'def' : defense,
                    'spe' : speed,
                    'spA' : spAttack,
                    'spD' : spDefense,
                    'types' : types,
                    'pp' : pp,
                    'status1' : status1,
                    'status2' : status2,
                    'lvl' : lvl,
                    'exp' : exp,
                    'statChanges' : statChanges,
                    'hp' : hp,
                    'maxHP' : maxHP,
                    'ability' : ability,
                    'moves' : moves,
                    'holdItem' : holdItem,
                    }
            if not self.double_battle :
                playerMon.append(poke)
            else :
                enemyMon.append(poke)
        if not self.double_battle :
            enemyMon.append(playerMon.pop(-1))
        
        self.double_battle = False

        return [playerMon,enemyMon,finishBattle]
        
    
        





    

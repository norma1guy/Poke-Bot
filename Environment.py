import posix_ipc
import mmap
import struct
from Memory import Memory
from Map import Map
from tensordict import TensorDict, TensorDictBase
from tensordict.nn import TensorDictModule
from torchrl.data import DiscreteTensorSpec,BoundedTensorSpec, CompositeSpec, UnboundedDiscreteTensorSpec,UnboundedContinuousTensorSpec
from torchrl.envs import (
    CatTensors,
    EnvBase,
    Transform,
    TransformedEnv,
    UnsqueezeTransform,
)
from typing import Optional
from torchrl.envs.transforms.transforms import _apply_to_composite
from torchrl.envs.utils import check_env_specs, step_mdp
import torch

class Environment(EnvBase) :

    def __init__(self,td_params=None,seed=None,device='cuda'):

        super().__init__(device=device,batch_size=[])
        self._make_spec()
        if seed is None:
            seed = torch.empty((), dtype=torch.int64).random_().item()
        self.set_seed(seed)
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
        self.input = {'A' : 0,'B' : 1,'Up' : 2,'Down' : 3, 'Left' : 4,'Right' : 5,'Select' : 6,'Start' : 7}
        

    def _get_state(self):
        self.is_battle = 1  if self.ewram.read_u32_le(0x22fec) != 0 else 0

        mapState = self.get_coords()
        badges = self.get_badges()
        party = self.get_party()
        hms = self.get_hms()
        player_battle_state,enemy_battle_state = self.get_battle_info()
        #print(enemy_battle_state)
        out = TensorDict(
            {
                'inbattle' : torch.tensor([self.is_battle],dtype=torch.int64,device=self.device),
                'playerpokemon' : player_battle_state,
                'enemypokemon' : enemy_battle_state,
                'map' : mapState,
                'badge' : badges,
                'party' : party,
                'hms' : hms,
            },
            batch_size=[]
        )
        
        return out.to(device=self.device)
    
    def _make_spec(self):

        self.observation_spec = CompositeSpec(
            inbattle = DiscreteTensorSpec(2, shape=(1,), dtype=torch.int64),
            playerpokemon = CompositeSpec(
                att = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                defn = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                spe = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                spA = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                spD = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                types = UnboundedDiscreteTensorSpec(shape=(2,2),dtype=torch.int64),
                pp = UnboundedDiscreteTensorSpec(shape=(2,4),dtype=torch.int64),
                statChanges = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                status1 = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                lvl = DiscreteTensorSpec(
                    n=101,
                    shape=(2,),
                    dtype=torch.int64,
                ),
                exp = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                hp = UnboundedContinuousTensorSpec(shape=(2,),dtype=torch.float32),
                ability = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                moves = UnboundedDiscreteTensorSpec(shape=(2,4),dtype=torch.int64),
                holdItem = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
                species = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),

            ),
            enemypokemon = CompositeSpec(
                hp = UnboundedContinuousTensorSpec(shape=(2,),dtype=torch.float32),
                lvl = DiscreteTensorSpec(
                    n=101,
                    shape=(2,),
                    dtype=torch.int64,
                ),
                status1 = UnboundedDiscreteTensorSpec(shape=(2,),dtype=torch.int64),
            ),
            map = UnboundedDiscreteTensorSpec(shape=(55,),dtype=torch.int64),
            badge = DiscreteTensorSpec(
                n=2,
                shape=(8,),
                dtype=torch.int64,
            ),
            party = CompositeSpec(
                status = UnboundedDiscreteTensorSpec(shape=(6,),dtype=torch.int64),
                level = DiscreteTensorSpec(
                    n=101,
                    shape=(6,),
                    dtype=torch.int64,
                ),
                hp = UnboundedContinuousTensorSpec(shape=(6,),dtype=torch.float32),
            ),
            hms = DiscreteTensorSpec(
                n=2,
                shape=(8,),
                dtype=torch.int64,
            ),
        )

        self.action_spec = DiscreteTensorSpec(
            n=8,
            shape=(1,),
            dtype=torch.int64,
        )

        self.reward_spec = UnboundedContinuousTensorSpec()


    def _set_seed(self, seed: Optional[int]):
        rng = torch.manual_seed(seed)
        self.rng = rng

    def calc_reward(self,prevState,nextState) :
        reward = 0
        # Badge reward
        if prevState is None :
            pass
        elif nextState['badge'].sum() > prevState['badge'].sum() :
            reward += 10 
        
        # Movement reward
        if prevState is None :
            reward += 0.1
        elif not torch.equal(nextState['map'],prevState['map']) :
            reward += 0.1

        # HMs reward
        if prevState is None :
            pass
        elif nextState['hms'].sum() > prevState['hms'].sum() :
            reward += 10
        
        
        return torch.tensor(reward, dtype=torch.float32,device=self.device)
    
    def _step(self,tensordict) :
        action = tensordict.get('action')
        prev_obs = TensorDict({
            'inbattle' : tensordict.get('inbattle'),
            'playerpokemon' : tensordict.get('playerpokemon'),
            'enemypokemon' : tensordict.get('enemypokemon'),
            'map' : tensordict.get('map'),
            'badge' : tensordict.get('badge'),
            'party' :tensordict.get('party'),
            'hms' : tensordict.get('hms'),
            },
            batch_size=[],
            device=self.device)
        self.luaFlag.acquire()
        self.mm[:4] = struct.pack("I", action.item())
        next_obs = self._get_state()
        reward = self.calc_reward(prev_obs,next_obs)
        self.pyFlag.release()
        out = TensorDict(
            {
                'inbattle' : next_obs['inbattle'],
                'playerpokemon' : next_obs['playerpokemon'],
                'enemypokemon' : next_obs['enemypokemon'],
                'map' : next_obs['map'],
                'badge' : next_obs['badge'],
                'party' :next_obs['party'],
                'hms' : next_obs['hms'],
                'reward' : reward,
                'done' : (next_obs['party']['hp'] <= 0).all()
            },
            batch_size=[]
        )
        return out.to(device=self.device)
    
    def _reset(self, tensordict):
        self.luaFlag.acquire()
        if tensordict is None :
            tensordict = TensorDict({
            },batch_size=[])
        out = tensordict.clone()
        self.mm[:4] = struct.pack('I', 8)
        self.pyFlag.release()
        #out['observation'] = self._get_state()
        return self._get_state()
            

    
    def get_hms(self) :
        hms = [0] * 8
        saveBlockAddr = self.iwram.read_u32_le(0x5d8c) - 0x2000000 # Using saveBlockPtr from IWRAM
        #print(saveBlockAddr)
        TMHMBagPocket = saveBlockAddr + 0x690
        for i in range(8) :
            hms[i] = 1 if self.ewram.read_u16_le(TMHMBagPocket + 339 + 4 * i) else 0

        return torch.tensor(hms,dtype=torch.int64,device=self.device)

   
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
        return torch.tensor(pos,dtype=torch.int64,device=self.device)
    
    def get_party(self):

        partyCount = self.ewram.read_u8(0x244e9)
        party = { 
                    'status' : [],
                    'level' : [],
                    'hp' : [],                  
                }
        partyAddr = 0x244ec
        structSize = 104 # size of each Pokemon struct

        for i in range(6):
            if i < partyCount :
                pokemon = partyAddr + i * structSize
                status = self.ewram.read_u32_le(pokemon + 0x50)
                level = self.ewram.read_u8(pokemon + 0x54)
                hp = self.ewram.read_u16_le(pokemon + 0x56)
                maxhp = self.ewram.read_u16_le(pokemon + 0x58)
                party['status'].append(status)
                party['level'].append(level)
                party['hp'].append(hp/maxhp)
            else :
                for j in ['status','level','hp'] :
                    party[j].append(0)

        #print(party)
        out = TensorDict({
            'status': torch.tensor(party['status'],dtype=torch.int64,device=self.device),
            'hp': torch.tensor(party['hp'],dtype=torch.float32,device=self.device),
            'level': torch.tensor(party['level'],dtype=torch.int64,device=self.device),
            },
            batch_size=[]
        )

        return out.to(device=self.device)
    
    def get_badges(self):
        badges = [0] * 8
        gym_flag = 0x867
        for i in range(8) :
            badges[i] = 1 if self.ewram.read_flag(gym_flag) else 0
            gym_flag += 1

        return torch.tensor(badges,dtype=torch.int64,device=self.device)
    
    def get_battle_info(self):
        gBattleMons = 0x24084 # Max can have 4 BattlePokemon(88 bytes each)
        sizeBattlePokemon = 88
        #gEnemyPartyCount = self.ewram.read_u8(0x244ea)
        #gPlayerPartyCount = self.ewram.read_u8(0x244e9)
        #gCurrentMove = self.ewram.read_u16(0x0241ea)
        #gBattlerAttacker = self.ewram.read_u8(0x2420b)
        #gBattlerTarget = self.ewram.read_u8(0x2420c)
        #gLastMoves = [self.ewram.read_u16(hex(0x24248 + i * 2)) for i in range(4)]
        gBattlerCount = self.ewram.read_u8(0x2406c)
        if gBattlerCount > 2 :
            self.double_battle = True
        playerMon = {'species' : [],
                     'att' : [],
                     'defn' : [],
                     'spe' : [],
                     'spA' : [],
                     'spD' : [],
                     'types' : [],
                     'pp' : [],
                     'status1' : [],
                     'lvl' : [],
                     'exp' : [],
                     'statChanges' : [],
                     'hp' : [],
                     'ability' : [],
                     'moves' : [],
                     'holdItem' : []
                    }
        enemyMon = { 'status1' : [],
                    'status2' : [],
                    'lvl' : [],
                    'hp' : [],
                    }
                
        finishBattle = 0
        for i in range(gBattlerCount) :
            mon = gBattleMons + i * sizeBattlePokemon
            attack = self.ewram.read_u16_le(mon + 0x2)
            defense = self.ewram.read_u16_le(mon + 0x4)
            speed = self.ewram.read_u16_le(mon + 0x6)
            spAttack = self.ewram.read_u16_le(mon + 0x8)
            spDefense = self.ewram.read_u16_le(mon + 0xa)
            types = [self.ewram.read_u8(mon + 0x21),self.ewram.read_u8(mon + 0x22)]
            pp = [self.ewram.read_u8(mon + 0x24 + i) for i in range(4)]
            statChanges = self.ewram.read_s8(mon + 0x18)
            status1 = self.ewram.read_u32_le(mon + 0x4C)
            lvl = self.ewram.read_u8(mon + 0x2A)
            exp = self.ewram.read_u32_le(mon + 0x44)
            maxHP = self.ewram.read_u16_le(mon + 0x2C)
            hp = self.ewram.read_u16_le(mon + 0x28)
            ability = self.ewram.read_u8(mon + 0x20)
            moves = [self.ewram.read_u16_le(mon + 0x0C + 2 * i) for i in range(4)]
            holdItem = self.ewram.read_u16_le(mon + 0x2E)
            species = self.ewram.read_u16_le(mon)

            if self.double_battle :
                if i < 2 : 
                    playerMon['att'].append(attack)
                    playerMon['defn'].append(defense)
                    playerMon['spe'].append(speed)
                    playerMon['spA'].append(spAttack)
                    playerMon['spD'].append(spDefense)
                    playerMon['types'].append(types)
                    playerMon['pp'].append(pp)
                    playerMon['statChanges'].append(statChanges)
                    playerMon['status1'].append(status1)
                    playerMon['lvl'].append(lvl)
                    playerMon['exp'].append(exp)
                    playerMon['hp'].append(hp/maxHP)
                    playerMon['ability'].append(ability)
                    playerMon['moves'].append(moves)
                    playerMon['holdItem'].append(holdItem)
                    playerMon['species'].append(species)
                else :
                    enemyMon['hp'].append(hp/maxHP)
                    enemyMon['lvl'].append(lvl)
                    enemyMon['status1'].append(status1)
            else :
                if i < 1 :
                    playerMon['att'].append(attack)
                    playerMon['defn'].append(defense)
                    playerMon['spe'].append(speed)
                    playerMon['spA'].append(spAttack)
                    playerMon['spD'].append(spDefense)
                    playerMon['types'].append(types)
                    playerMon['pp'].append(pp)
                    playerMon['statChanges'].append(statChanges)
                    playerMon['status1'].append(status1)
                    playerMon['lvl'].append(lvl)
                    playerMon['exp'].append(exp)
                    playerMon['hp'].append(hp/maxHP)
                    playerMon['ability'].append(ability)
                    playerMon['moves'].append(moves)
                    playerMon['holdItem'].append(holdItem)
                    playerMon['species'].append(species)
                else :
                    enemyMon['hp'].append(hp/maxHP)
                    enemyMon['lvl'].append(lvl)
                    enemyMon['status1'].append(status1)
        
        self.double_battle = False
        
        for i in range(2 - len(playerMon['att'])) :
            playerMon['att'].append(0)
            playerMon['defn'].append(0)
            playerMon['spe'].append(0)
            playerMon['spA'].append(0)
            playerMon['spD'].append(0)
            playerMon['types'].append([0,0])
            playerMon['pp'].append([0,0,0,0])
            playerMon['statChanges'].append(0)
            playerMon['status1'].append(0)
            playerMon['lvl'].append(0)
            playerMon['exp'].append(0)
            playerMon['hp'].append(0)
            playerMon['ability'].append(0)
            playerMon['moves'].append([0,0,0,0])
            playerMon['holdItem'].append(0)
            playerMon['species'].append(0)

        for i in range(2 - len(enemyMon['lvl'])) :
            enemyMon['hp'].append(0)
            enemyMon['lvl'].append(0)
            enemyMon['status1'].append(0)

        #print(len(playerMon['att']),len(enemyMon['hp']))
        pM = TensorDict({
            'att' : torch.tensor(playerMon['att'],dtype=torch.int64,device=self.device),
            'defn' : torch.tensor(playerMon['defn'],dtype=torch.int64,device=self.device),
            'spe' : torch.tensor(playerMon['spe'],dtype=torch.int64,device=self.device),
            'spA' : torch.tensor(playerMon['spA'],dtype=torch.int64,device=self.device),
            'spD' : torch.tensor(playerMon['spD'],dtype=torch.int64,device=self.device),
            'types' : torch.tensor(playerMon['types'],dtype=torch.int64,device=self.device),
            'pp' : torch.tensor(playerMon['pp'],dtype=torch.int64,device=self.device),
            'statChanges' : torch.tensor(playerMon['statChanges'],dtype=torch.int64,device=self.device),
            'status1' : torch.tensor(playerMon['status1'],dtype=torch.int64,device=self.device),
            'lvl' : torch.tensor(playerMon['lvl'],dtype=torch.int64,device=self.device),
            'exp' : torch.tensor(playerMon['exp'],dtype=torch.int64,device=self.device),
            'hp' : torch.tensor(playerMon['hp'],dtype=torch.float32,device=self.device),
            'ability' : torch.tensor(playerMon['ability'],dtype=torch.int64,device=self.device),
            'moves' : torch.tensor(playerMon['moves'],dtype=torch.int64,device=self.device),
            'holdItem' : torch.tensor(playerMon['holdItem'],dtype=torch.int64,device=self.device),
            'species' : torch.tensor(playerMon['species'],dtype=torch.int64,device=self.device),
            },
            batch_size=[]
        ).to(device=self.device)

        eM = TensorDict({
            'hp' : torch.tensor(enemyMon['hp'],dtype=torch.float32,device=self.device),
            'lvl' : torch.tensor(enemyMon['lvl'],dtype=torch.int64,device=self.device),
            'status1' : torch.tensor(enemyMon['status1'],dtype=torch.int64,device=self.device),
            },
            batch_size=[]
        ).to(device=self.device)

        

        return (pM,eM)
        
    
        





    

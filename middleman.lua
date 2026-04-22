--Set memory domain to EWRAM
memory.usememorydomain("EWRAM")
print(memory.getcurrentmemorydomain())

--Load functions
package.cpath = package.cpath .. ";/home/pmv/Desktop/RL/Bizhawk-2.11-linux-x64/Lua/RL/?.so"
mmap = require('myshm')
shm = mmap.create_shm()
input_map = {'Up','Down','Left','Right','A','B','Start','Select'}

while true do
    inputs = {['Up'] = false,['Down'] = false,['Left'] = false,['Right'] = false,['A'] = false,['B'] = false,['Select'] = false,['Start'] = false}
    memory.usememorydomain("EWRAM")
    local ewram_map = memory.readbyterange_raw(0x0,256 * 1024)
    memory.usememorydomain("IWRAM")
    local iwram_map = memory.readbyterange_raw(0x0, 32 * 1024)
    shm:write(ewram_map,iwram_map)
    gui.text(10, 10, "State shared")
    local input = shm:read()
    inputs[input_map[input]] = true
    joypad.set(inputs)
    emu.frameadvance()
end
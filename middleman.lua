--Set memory domain to EWRAM
memory.usememorydomain("EWRAM")
print(memory.getcurrentmemorydomain())

--Load functions
package.cpath = package.cpath .. ";/home/pmv/Desktop/RL/Bizhawk-2.11-linux-x64/Lua/RL/?.so"
mmap = require('myshm')
shm = mmap.create_shm()
while true do

    local ram_map = memory.readbyterange(0x2000000,256 * 1024)
    local ram_data = string.char(table,unpack(ram_map))
    shm:write(ram_data)
    gui.text(10, 10, "X: " .. coords.x)
    gui.text(10, 25, "Y: " .. coords.y)
    emu.frameadvance()
end
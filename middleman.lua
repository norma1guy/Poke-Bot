--Set memory domain to EWRAM
memory.usememorydomain("EWRAM")
print(memory.getcurrentmemorydomain())

--Load functions
dofile('playerCoords.lua')
package.cpath = package.cpath .. ";/home/pmv/Desktop/RL/Bizhawk-2.11-linux-x64/Lua/RL/?.so"
mmap = require('myshm')
shm = mmap.create_shm()
while true do

    coords = playerCoords()
    shm:write(string.format("%d,%d",coords.x,coords.y))
    gui.text(10, 10, "X: " .. coords.x)
    gui.text(10, 25, "Y: " .. coords.y)
    emu.frameadvance()
end
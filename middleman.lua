--Set memory domain to EWRAM
memory.usememorydomain("EWRAM")
print(memory.getcurrentmemorydomain())

--Load functions
dofile('playerCoords.lua')
mmap = require('myshm')
shm = mmap.create_shm()
while true do

    coords = playerCoords()
    shm:write(coords)
    gui.text(10, 10, "X: " .. coords.x)
    gui.text(10, 25, "Y: " .. coords.y)
    emu.frameadvance()
end
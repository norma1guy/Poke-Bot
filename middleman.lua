--Load functions
package.cpath = package.cpath .. ";/home/pmv/Desktop/RL/CustomBiz/BizHawk/output/Lua/RL/?.so"
mmap = require('myshm')
shm = mmap.create_shm()
input_map = {[0] = 'Up',[1] = 'Down',[2] = 'Left',[3] = 'Right',[4] = 'A',[5] = 'B',[6] = 'Start',[7] = 'Select',[8] = 'load'}
frames = 0
local socket = require("socket")

local function createTimer(delay,callback)
    local start = socket.gettime()
    return {
        check = function()
            if socket.gettime() - start >= delay then
                callback()
                return true
            end
            return false
        end,
        cancel = function()
            start = nil
        end
    }
end

while true do
    -- Skip 2 frames ( Can also not skip frames)
    print(frames)
    memory.usememorydomain("EWRAM")
    text_active = memory.read_u8(0x201c8)
    if frames % 30 == 0 and text_active == 0 then 
        inputs = {['Up'] = false,['Down'] = false,['Left'] = false,['Right'] = false,['A'] = false,['B'] = false,['Select'] = false,['Start'] = false}
        local ewram_map = memory.readbyterange_raw(0x0,256 * 1024)
        memory.usememorydomain("IWRAM")
        local iwram_map = memory.readbyterange_raw(0x0, 32 * 1024)
        --socket.sleep(10)
        shm:write(ewram_map,iwram_map)
        gui.text(10, 10, "State shared")
        local input = shm:read()
        gui.text(20,20,"Action taken " .. input_map[input] .. "!")
        if input == 8 then 
            savestate.loadslot(10)
        else
            inputs[input_map[input]] = true
            joypad.set(inputs)
            frames = frames + 1
        end
        frames = 0
    end
    emu.frameadvance()
    frames = frames + 1
end
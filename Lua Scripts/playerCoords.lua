-- Function to get the player coordinates

function playerCoords()
    playerAvatar = 0x37590
    objectEvents = 0x37350
    objectSize = 0x24
    playerEvent = memory.read_u8(playerAvatar + 5)
    playerObject = objectEvents + playerEvent * objectSize

    xCoord = memory.read_s16_le(playerObject + 0x10)
    yCoord = memory.read_s16_le(playerObject + 0x12)

    return {x = xCoord,y = yCoord}
end

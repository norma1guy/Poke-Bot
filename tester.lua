from 
mmap = require('myshm')
shm = mmap.create_shm()

while true do
    shm:write('Hello Python!')
    print(shm:read())

end
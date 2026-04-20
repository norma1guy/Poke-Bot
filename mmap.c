#include <stdio.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <semaphore.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>
#define SIZE 288 * 1024
#define name "/RAM_MAP"

typedef struct {
    uint32_t state;
    uint32_t size;
    char buffer[SIZE];
} shm;

typedef struct {
    shm *ptr;
    sem_t *lua;
    sem_t *py;
} handler;


static int create_shm(lua_State *L){

    //Release any old semaphores
    sem_unlink("/lua_to_py");
    sem_unlink("/py_to_lua");


    int shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) return luaL_error(L,"shm_open failed");


    if(ftruncate(shm_fd,sizeof(shm)) == -1) {
        close(shm_fd);
        return luaL_error(L,"ftruncate failed");
    }

    shm *ptr = mmap(NULL,sizeof(shm),PROT_READ | PROT_WRITE, MAP_SHARED,shm_fd,0);
    close(shm_fd);
    if (ptr == MAP_FAILED) return luaL_error(L,"mmap failed");


    sem_t *lua_to_py = sem_open("/lua_to_py", O_CREAT, 0666,0);
    sem_t *py_to_lua = sem_open("/py_to_lua", O_CREAT, 0666,1);
    if(lua_to_py == SEM_FAILED ){
        munmap(ptr, sizeof(shm));
        return luaL_error(L, "sem_open lua_to_py failed");
    }
    if(py_to_lua == SEM_FAILED) {
        munmap(ptr, sizeof(shm));
        sem_close(lua_to_py);
        return luaL_error(L, "sem_open failed");
    }

    handler *handle = lua_newuserdata(L, sizeof(handler));

    handle->ptr = ptr;
    handle->lua = lua_to_py;
    handle->py = py_to_lua;
    luaL_getmetatable(L, "shm_handler");
    lua_setmetatable(L, -2);

    return 1;
}

static int open_shm(lua_State *L){

    int shm_fd = shm_open(name,O_RDWR,0666);
    if (shm_fd == -1) return luaL_error(L,"shm_open failed");

    shm *ptr = mmap(NULL,sizeof(shm),PROT_READ | PROT_WRITE,MAP_SHARED, shm_fd,0);
    close(shm_fd);
    if(ptr == MAP_FAILED) return luaL_error(L, "mmap failed");
    sem_t *lua = sem_open("/lua_to_py",0);
    sem_t *py = sem_open("/py_to_lua",0);
    if(lua == SEM_FAILED ){
        munmap(ptr, sizeof(shm));
        return luaL_error(L, "sem_open lua_to_py failed");
    }
    if(py == SEM_FAILED) {
        munmap(ptr, sizeof(shm));
        sem_close(lua);
        return luaL_error(L, "sem_open failed");
    }

    handler *handle = lua_newuserdata(L, sizeof(handler));
    handle->ptr = ptr;
    handle->lua = lua;
    handle->py = py;
    

    return 1;
}


static int handler_gc(lua_State *L) {
    handler *h = luaL_checkudata(L, 1, "shm_handler");
    if(h->ptr) munmap(h->ptr, sizeof(shm));
    if(h->lua) sem_close(h->lua);
    if(h->py) sem_close(h->py);
    return 0;
}

static int shm_write(lua_State *L) {
    handler *h = luaL_checkudata(L, 1, "shm_handler");
    //const char *msg = luaL_checkstring(L, 2);
    sem_wait(h->py);

    size_t len;
    const char *msg = luaL_checklstring(L,2,&len);
    if(len >= SIZE) len = SIZE;
    
    memcpy(h->ptr->buffer, msg, len);
    h->ptr->size = len;
    sem_post(h->lua);

    return 0;
}

static int shm_read(lua_State *L) {
    handler *h = luaL_checkudata(L, 1, "shm_handler");
    //sem_wait(h->py);
    lua_pushlstring(L, h->ptr->buffer,h->ptr->size);
    //sem_post(h->lua);
    return 1;
}

int luaopen_myshm(lua_State *L) {
    luaL_newmetatable(L, "shm_handler");
    lua_newtable(L);
    lua_pushcfunction(L,shm_write);
    lua_setfield(L,-2,"write");
    lua_pushcfunction(L,shm_read);
    lua_setfield(L,-2,"read");
    lua_setfield(L,-2,"__index");
    lua_pushcfunction(L, handler_gc);
    lua_setfield(L, -2, "__gc");
    lua_pop(L, 1);

    static const luaL_Reg funcs[] = {
        {"create_shm", create_shm},
        {"open_shm", open_shm},
        {NULL, NULL}
    };
    luaL_newlib(L, funcs);
    return 1;
}
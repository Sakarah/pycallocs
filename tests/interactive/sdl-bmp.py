from elflib import char
from elflib.libSDL2 import *
from elflib.libc import clock
import atexit
import math
cstr = char.array

# == MACROS ==
SDL_INIT_VIDEO = 0x20
SDL_WINDOWPOS_UNDEFINED = 0x1fff0000
SDL_QUIT = 0x100
SDL_LoadBMP = lambda f: SDL_LoadBMP_RW(SDL_RWFromFile(f, cstr("rb")), 1)
# == End of macros ==

if SDL_Init(SDL_INIT_VIDEO) != 0:
    exit(1)
atexit.register(SDL_Quit)

win = SDL_CreateWindow(cstr("Hello from Python"), 
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 256, 256, 0)
if win is None:
    exit(1)

ren = SDL_CreateRenderer(win, -1, 0)
if ren is None:
    SDL_DestroyWindow(win)
    exit(2)

bitmapSurface = SDL_LoadBMP(cstr("troll.bmp"))
if bitmapSurface is None:
    SDL_DestroyWindow(win)
    SDL_DestroyRenderer(ren)
    exit(3)
bitmapTex = SDL_CreateTextureFromSurface(ren, bitmapSurface)
SDL_FreeSurface(bitmapSurface)

while True:
    ev = SDL_Event()
    if (SDL_PollEvent(ev)):
        if ev.type == SDL_QUIT:
            break

    t = clock() / 100000
    r = int((1 + math.sin(t + 0/3 * math.pi)) / 2 * 255)
    g = int((1 + math.sin(t + 2/3 * math.pi)) / 2 * 255)
    b = int((1 + math.sin(t + 4/3 * math.pi)) / 2 * 255)
    SDL_SetRenderDrawColor(ren, r, g, b, 255)
    SDL_RenderClear(ren)
    SDL_RenderCopy(ren, bitmapTex, None, None)
    SDL_RenderPresent(ren)

SDL_DestroyTexture(bitmapTex)
SDL_DestroyRenderer(ren)
SDL_DestroyWindow(win)

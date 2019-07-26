from elflib import char
from elflib.libSDL2 import *
from elflib.libpng import *
from elflib.libc import fopen, clock
import atexit
import math
cstr = char.array

# == MACROS ==
PNG_LIBPNG_VER_STRING = cstr("1.6.37")
PNG_COLOR_TYPE_RGBA = 0x6
SDL_INIT_VIDEO = 0x20
SDL_WINDOWPOS_UNDEFINED = 0x1fff0000
SDL_PIXELFORMAT_RGBA32 = 0x16762004
SDL_TEXTUREACCESS_STATIC = 0
SDL_BLENDMODE_BLEND = 0x1
SDL_QUIT = 0x100
# == End of macros ==

png_file = fopen(cstr("dices.png"), cstr("rb"))
if png_file is None:
    raise FileNotFoundError("failed to open png file")

png_reader = png_create_read_struct(PNG_LIBPNG_VER_STRING, None, None, None)
if png_reader is None:
    raise RuntimeError("failed to create png read struct")

png_info = png_create_info_struct(png_reader)
if png_info is None:
    raise RuntimeError("failed to create png info struct")

png_init_io(png_reader, png_file)
png_read_info(png_reader, png_info)

width = png_get_image_width(png_reader, png_info)
height = png_get_image_height(png_reader, png_info)
row_bytes = png_get_rowbytes(png_reader, png_info)

color_type = ord(png_get_color_type(png_reader, png_info))
bit_depth = ord(png_get_bit_depth(png_reader, png_info))
if color_type != PNG_COLOR_TYPE_RGBA and bit_depth != 8:
    raise RuntimeError("png file do not have the right image format")

imgbytes = unsigned_char_8.array(row_bytes * height)
imgrows = unsigned_char_8.ptr.array(height)
for row in range(height):
    imgrows[row] = imgbytes[row_bytes*row:row_bytes*(row+1)]

png_read_image(png_reader, imgrows)

png_read_end(png_reader, None)
png_destroy_read_struct(png_reader, png_info, None)

if SDL_Init(SDL_INIT_VIDEO) != 0:
    raise RuntimeError("failed to init SDL")
atexit.register(SDL_Quit)

win = SDL_CreateWindow(cstr("PNG display"),
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, 0)
if win is None:
    raise RuntimeError("failed to create window")

ren = SDL_CreateRenderer(win, -1, 0)
if ren is None:
    SDL_DestroyWindow(win)
    raise RuntimeError("failed to create renderer")

img = SDL_CreateTexture(ren, SDL_PIXELFORMAT_RGBA32, SDL_TEXTUREACCESS_STATIC, width, height)
SDL_UpdateTexture(img, None, imgbytes, row_bytes)
SDL_SetTextureBlendMode(img, SDL_BLENDMODE_BLEND)

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
    SDL_RenderCopy(ren, img, None, None)
    SDL_RenderPresent(ren)

SDL_DestroyTexture(img)
SDL_DestroyRenderer(ren)
SDL_DestroyWindow(win)

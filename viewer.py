#!/usr/bin/env python3

import struct
from contextlib import contextmanager
from typing import Self
from typing import BinaryIO
from dataclasses import dataclass
import codecs

import codec_cp220

import pygame


PYGAME_FPS=60


@contextmanager
def lock_surface(s : pygame.Surface):
    s.lock()
    try:
        yield s
    finally:
        s.unlock()


@dataclass
class DeepRedFase:
    level_width : int
    something_count : int
    level_height : int
    data : bytes

    @classmethod
    def from_file(cls, f: BinaryIO) -> Self:
        header_b = f.read(0xa)

        level_width, something_count, level_height, data_size  = struct.unpack("<HHHI", header_b)

        data = f.read(data_size)
        assert len(data) == data_size

        return cls(level_width, something_count, level_height, data)


    def get_column(self, idx):

        offset = idx * 8*self.level_height

        result = []
        for x in range(self.level_height):
            a,b = struct.unpack_from("<II", self.data, offset)
            offset += 8
            result.append( (a,b) )
        return result


def load_level(level_num):

    level_config = []
    with open(f"game/MAPAS/{level_num}.DAT", 'rb') as f:
        data = f.read()
        # print(data)
        data = data.splitlines()
        # print(data)
        
        for line in data:
            line = codecs.decode(line, encoding='cp220')
            level_config.append(line)

    print("loading gfx...")
    with open("game/"+level_config[0], 'rb') as f:
        palette_b = f.read(0x300)
        header_b = f.read(5)
        _, gfx_size, = struct.unpack("<BI", header_b)
        gfx_data = f.read(gfx_size)


    palette = []
    for idx in range(256):
        r,g,b = struct.unpack_from("<BBB",palette_b, idx*3)
        r<<=2
        g<<=2
        b<<=2
        palette.append( (r,g,b, 0xff) )
    
    tile_size_bytes = 16*16
    tile_by_id = {}
    idx = 1
    while True:
        tile_offset = (idx-1)*( 16*16 ) 
        if tile_offset >= len(gfx_data):
            break

        s = pygame.Surface( (16, 16), depth=8)
        s.set_palette(palette)
        # s.fill( 2 )

        with pygame.PixelArray(s) as pxarray:
            for y in range(16):
                for x in range(16):
                    pxarray[x,y] = gfx_data[ tile_offset + x + y*16   ]
            
        tile_by_id[idx] = s

        idx += 1

    print("done.")


    print("loading level...")
    with open(f"game/MAPAS/FASE{level_num}.PC1", "rb") as f:
        fase = DeepRedFase.from_file(f)
    print("done.")

    return tile_by_id, fase


def main():

    codec_cp220.load()

    pygame.init()
    pygame.font.init()

    pygame.display.set_caption('Deep Red Level Viewer')

    screen = pygame.display.set_mode( (0xAD*16, 0x30*16) )

    root_clock = pygame.time.Clock()

    my_font = pygame.font.SysFont("comicsansms", 8)


    level_num = 1
    tile_by_id, fase = load_level(level_num) 

    s_by_number = {}


    show_meta = False

    game_running = True

    while game_running:
        screen.fill( (0x20,0,0x20) )


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                elif event.key == pygame.K_LEFT:
                    new_level = level_num - 1
                    try:
                        tile_by_id, fase = load_level(new_level) 
                        level_num = new_level
                    except:
                        pass
                elif event.key == pygame.K_RIGHT:
                    new_level = level_num + 1
                    try:
                        tile_by_id, fase = load_level(new_level) 
                        level_num = new_level
                    except:
                        pass
                elif event.key == pygame.K_m:
                    show_meta = not show_meta


        x = 0
        y = 0

        bset = set()

        for idx  in range(0, fase.level_width):
            y = 0
            for a,b in fase.get_column(idx):
                bset.add(b&0xff)
                if a:
                    screen.blit( tile_by_id[a], (x,y) )

                if show_meta:

                    if b not in s_by_number:
                        s = my_font.render(f"{b:x}", True, (0xff,0xff,0, 0xff))
                        s_by_number[b] = s
                    
                    if b:
                        screen.blit( s_by_number[b], (x,y))

                y += 16
            x += 16

        pygame.display.flip()
        root_clock.tick(PYGAME_FPS)


    pygame.quit()


if __name__ == "__main__":
    main()

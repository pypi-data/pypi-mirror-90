#!/usr/bin/env python3

"""
Convert JSON level file into a binary level file.
It is assumed that the level map can be larger than the screen, therefore
we define a viewport size and the initial position of the viewport. The
dimension and position are all defined in tiles.

flags:

bit 0: not set -> big endian, set -> little endian

Header (32 bytes)

'RATR0LVL'     byte 0-7   identifier
version        byte 8     version
flags          byte 9     special flags
width          byte 10-11 level width in tiles
height         byte 12-13 level height in tiles
vp_width       byte 14-15 viewort width in tiles
vp_height      byte 16-17 viewort height in tiles
init_vp_row    byte 18-19 initial row position for viewport
init_vp_col    byte 20-21 initial column position for viewport
reserved       byte 22-23 reserved, currently only padding
checksum       byte 24-27 checksum of the entire file

level_data     <width * height pairs of words  (tile_i, tile_j)>

Note:

a pair where tile_i is 0xffff (set tile_j to that value, too),
should be considered a null tile and is not rendered

For license, see gpl-3.0.txt
"""
import struct
import json

def write_level(level, outfile, verbose):
    with open(outfile, 'wb') as out:
        out.write(b'RATR0LVL')
        out.write(bytes([1, 0]))
        height = len(level['map'])
        width = len(level['map'][0])
        checksum = 0

        # check if all rows have the same width
        for i, row in enumerate(level['map']):
            if len(row) != width:
                raise Exception('width of row %d != %d (actual width: %d)' % (i, width, len(row)))
        out.write(struct.pack(">H", width))
        out.write(struct.pack(">H", height))
        out.write(struct.pack(">H", level['viewport']['width']))
        out.write(struct.pack(">H", level['viewport']['height']))
        out.write(struct.pack(">H", level['viewport']['y']))
        out.write(struct.pack(">H", level['viewport']['x']))
        out.write(struct.pack(">H", 0))  # reserved (padding)

        out.write(struct.pack(">I", checksum))
        for i, row in enumerate(level['map']):
            for j, cell in enumerate(row):
                if len(cell) == 2:
                    tile_i, tile_j = cell
                    out.write(struct.pack(">H", tile_i))
                    out.write(struct.pack(">H", tile_j))
                else:
                    # this is a null cell
                    out.write(struct.pack(">H", 0xffff))
                    out.write(struct.pack(">H", 0xffff))

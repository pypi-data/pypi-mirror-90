#!/usr/bin/env python3
"""iled.py - TilED conversion tool

TilED is a great cross-platform tool to create level data. This conversion
tool converts the JSON data from TilED to generate level data for the
RATR0 engine.
"""
import json
import os
from PIL import Image

from ratr0.util import tiles, levels, png_util


def convert_tiles(intiles, indir, outfile, non_interleaved,
                  palette24, force_depth, verbose):
    imagepath = os.path.join(indir, intiles["image"])
    tile_width = intiles['tilewidth']
    tile_height = intiles['tileheight']
    im = Image.open(imagepath)
    colors = png_util.make_colors(im, force_depth, verbose)
    tiles.write_tiles(im, outfile, [tile_width, tile_height], colors,
                      palette24=palette24,
                      non_interleaved=non_interleaved,
                      create_mask=False,
                      verbose=verbose)


def chunks(l, k):
    for i in range(0, len(l), k):
        yield l[i: i + k]


def convert_level(inlevel, id2pos_map, outfile, verbose):
    if len(inlevel["layers"]) > 1:
        print("Warning: currently only a single layer is supported")
    inmap = inlevel["layers"][0]
    inmap_data = inmap["data"]
    rows = map(lambda r: map(lambda i: id2pos_map[i], r), chunks(inmap_data, inmap["width"]))
    rows = list([list(row) for row in rows])
    ratr0_level = {
        "name": "level",
        "viewport": {
            "x": 0, "y": 0,
            "width": inmap["width"],
            "height": inmap["height"]
        },
        "map":  rows
    }
    levels.write_level(ratr0_level, outfile, verbose)

def make_id2pos_map(intiles):
    columns = intiles["columns"]
    tile_count = intiles["tilecount"]
    tile_width = intiles["tilewidth"]
    tile_height = intiles["tileheight"]
    rows = int(tile_count / columns)
    # (RATR0 levels require (x, y) pairs)
    return { i + 1: (i % columns, int(i / columns)) for i in range(tile_count)}

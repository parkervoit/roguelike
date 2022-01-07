from typing import Tuple

import numpy as np

# Tile structure type compatble with Console.tiles_rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32), # denotes Unicode
        ("fg", "3B"), # 3 unsigned bytes for RGB
        ("bg", "3B"),
    ]
)

# Tile struct for statically defined tile data
tile_dt = np.dtype(
    [
        ("walkable", np.bool), # True if can be walked on
        ("transparent", np.bool), #true if tile doesn't obstruct FOV
        ("dark", graphic_dt), #graphics fro when tile is not in FOV
        ("light", graphic_dt), #for when the tile is in FOV
    ]
)

def new_tile(
    *, #enforce use of keywords so parameter order doesnt matter
    walkable: int,
    transparent: int, 
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    '''helper function for defining individual tile types'''
    return np.array((walkable, transparent, dark, light), dtype = tile_dt)
# SHROUD represents fog of war
SHROUD = np.array((ord(" "), (255,255,255), (0, 0, 0)), dtype = graphic_dt)
floor = new_tile(
    walkable = True, 
    transparent = True, 
    dark = (ord(" "), (255,255,255), (50, 50, 150)),
    light = (ord(" "), (255,255,255), (200, 180, 50)),
)

wall = new_tile(
    walkable = False, 
    transparent = False, 
    dark=(ord(" "), (255,255,255), (0, 0, 100)),
    light=(ord(" "), (255,255,255), (130,110,50))
)
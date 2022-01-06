import numpy as np
from tcod.console import Console

import tile_types

class GameMap: 
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value = tile_types.wall, order = 'F')
        self.visible = np.full((width, height), fill_value = False, order = "F")
        self.explored = np.full((width, height), fill_value = False, order = "F")

    def in_bounds(self, x:int, y: int) -> bool:
        '''Return True if x and y are inside the map bounds'''
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None:
        '''
        Renders the map
        
        if tile == visible, draw with light
        if tile == explored, draw with dark
        if tile != explored & tile != visible, draw with shroud
        '''        
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist = [self.tiles['light'], self.tiles['dark']],
            default = tile_types.shroud
        )
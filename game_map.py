from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity

class GameMap: 
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
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
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(x = entity.x, y = entity.y, string=entity.char, fg=entity.color)
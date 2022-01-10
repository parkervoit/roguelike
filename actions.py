from __future__ import annotations

import color 

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        '''return the engine this aciton belongs to'''
        return self.entity.gamemap.engine

    def perform(self) -> None:
        '''Perform this action with objects needed to determine its scope.
        self.engine is the scope the action is being performed in, while self.entity is the thing 
        performing the action. Must be overriden by action subclass'''
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
    @property
    def dest_xy(self) -> Tuple[int, int]:
        '''returns this actions destination'''
        return self.entity.x + self.dx, self.entity.y + self.dy
    
    @property 
    def blocking_entity(self) -> Optional[Entity]:
        '''return blocking entity at this location'''
        return self.engine.game_map.get_blocking_entity(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)
    
    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return
        
        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f'{self.entity.name.title()} attacks {target.name}'

        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f'{attack_desc} for {damage}!', attack_color
            )
            target.fighter.hp -= damage
        else: 
            self.engine.message_log.add_message(
                f'{attack_desc} but does nothing!', attack_color
            )
class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return #OOB
        if not self.engine.game_map.tiles['walkable'][dest_x, dest_y]:
            return #blocked tile
        if self.engine.game_map.get_blocking_entity(dest_x, dest_y):
            return #destination blocked
        
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self,) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
            
class WaitAction(Action):
    def perform(self) -> None:
        #print(f'The {self.entity.name} waits')
        pass

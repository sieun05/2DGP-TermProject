from pico2d import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import game_framework
from . import title_mode
from map import Map
from player import Player
# from grass import Grass
import game_world
from zombie import Zombie
from building import Building

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)
            pass

def init():
    global player

    map = Map()
    game_world.add_object(map, 0)

    player = Player(map)
    game_world.add_object(player, 1)

    game_world.add_collision_pair("player:zombie", player, None)
    game_world.add_collision_pair("player:building", player, None)
    game_world.add_collision_pair("zombie:building", None, None)

    zombies = [Zombie(map, player) for _ in range(10)]
    game_world.add_objects(zombies, 1)
    for zombie in zombies:
        game_world.add_collision_pair("player:zombie", None, zombie)
        game_world.add_collision_pair("zombie:building", zombie, None)

    buildings = [Building(map, 400, 300)]
    game_world.add_objects(buildings, 1)
    for building in buildings:
        game_world.add_collision_pair("player:building", None, building)
        for zombie in zombies:
            game_world.add_collision_pair("zombie:building", None, building)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

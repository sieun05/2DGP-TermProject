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
from map_data import *
import random
from car import Car


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

    # 플레이어가 이미 존재한다면 상태 초기화, 없다면 새로 생성
    if 'player' in globals() and player is not None:
        player.map = map  # 새로운 맵 참조 설정
        player.reset()  # 플레이어 상태 초기화
    else:
        player = Player(map)

    game_world.add_object(player, 1)

    game_world.add_collision_pair("player:zombie", player, None)
    game_world.add_collision_pair("player:building", player, None)
    game_world.add_collision_pair("zombie:building", None, None)
    game_world.add_collision_pair("zombie:zombie", None, None)
    game_world.add_collision_pair("zombie:gun", None, None)

    zombies = [Zombie(map, player, random.randint(0, 2400), random.randint(0,1800)) for _ in range(6)]
    game_world.add_objects(zombies, 1)
    for i, zombie in enumerate(zombies):
        game_world.add_collision_pair("player:zombie", None, zombie)
        game_world.add_collision_pair("zombie:building", zombie, None)
        game_world.add_collision_pair("zombie:gun", zombie, None)
        for other_zombie in zombies[i+1:]:
            game_world.add_collision_pair("zombie:zombie", zombie, other_zombie)

    buildings = [Building(map, *building_list[i], random.randint(0, 1), random.randint(0, 1)) for i in range(len(building_list)) if random.randint(0, 2) == 0]
    game_world.add_objects(buildings, 1)
    for building in buildings:
        game_world.add_collision_pair("player:building", None, building)
        for zombie in zombies:
            game_world.add_collision_pair("zombie:building", None, building)

    cars = [Car(map, *car_list[i], random.randint(0, 1), random.randint(0, 1)) for i in range(len(car_list)) if random.randint(0, 8) == 0]
    game_world.add_objects(cars, 1)


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

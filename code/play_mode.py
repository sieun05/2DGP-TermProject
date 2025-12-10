from pico2d import *

import game_framework
import lobby_mode
import gameover_mode
from map import Map
from player import Player
# from grass import Grass
import game_world
from building import Building
from map_data import *
import random
from car import Car
from zombie_spawner import ZombieSpawner
from player_ui import PlayerUI
import common
from big_car import Car3
from playmode_sound import BGM_Play


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            player.handle_event(event)
            pass

def init():
    global player, zombie_spawners, home_car_timer, home_car

    home_car_timer = get_time()
    home_car = None

    # 게임 월드 완전 초기화 (혹시 남아있는 객체들 제거)
    game_world.clear()

    player_ui = PlayerUI()
    game_world.add_object(player_ui, 2)

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
    # player와 car 충돌 페어 왼쪽에 player 등록 (우측은 각 car 객체가 추가됨)
    game_world.add_collision_pair("player:car", player, None)
    game_world.add_collision_pair("zombie:building", None, None)
    game_world.add_collision_pair("zombie:zombie", None, None)
    game_world.add_collision_pair("zombie:gun", None, None)
    game_world.add_collision_pair("player:car", player, None)
    game_world.add_collision_pair("player:homecar", player, None)

    buildings = [Building(map, *building_list[i], random.randint(0, 1), random.randint(0, 1)) for i in range(len(building_list)) if random.randint(0, 2) == 0]
    game_world.add_objects(buildings, 1)
    for building in buildings:
        game_world.add_collision_pair("player:building", None, building)
        game_world.add_collision_pair("zombie:building", None, building)

    cars = [Car(map, *car_list[i], random.randint(0, 1), random.randint(0, 1)) for i in range(len(car_list)) if random.randint(0, 8) == 0]
    game_world.add_objects(cars, 1)
    for car in cars:
        game_world.add_collision_pair("player:car", None, car)

    # 이전에 있던 좀비 스포너들(있다면) 정리
    if 'zombie_spawners' in globals() and zombie_spawners is not None:
        try:
            for s in zombie_spawners:
                if hasattr(s, 'clear'):
                    s.clear()
        except Exception:
            pass
        # 이전 리스트 참조 제거
        zombie_spawners = None

    # 좀비 스포너들을 완전히 새로 생성
    zombie_spawners = [ZombieSpawner(common.round, *zombie_spawner_list[i], map, player) for i in range(len(zombie_spawner_list))]
    game_world.add_objects(zombie_spawners, 0)

    # 플레이어 게임오버 푸시 플래그 초기화
    player.gameover_pushed = False

    print("Play mode initialized: All zombie spawners reset to initial state")

    bgm = BGM_Play()
    game_world.add_object(bgm, 0)


def finish():
    game_world.clear()
    pass

def update():
    global home_car_timer, home_car

    game_world.update()
    game_world.handle_collisions()

    # 플레이어 HP가 0 이하가 되면 게임오버 모드로 전환 (한 번만)
    if 'player' in globals() and player is not None and common.player_heart <= 0:
        if not getattr(player, 'gameover_pushed', False):
            print(f"Player heart {common.player_heart} <= 0 -> pushing gameover mode")
            player.gameover_pushed = True
            game_framework.change_mode(gameover_mode)

    if home_car is None and get_time() - home_car_timer >= 5.0:
        print('Spawning home car')
        home_car = Car3(player.map, *zombie_spawner_list[random.randint(0, len(zombie_spawner_list) - 1)])
        game_world.add_object(home_car, 1)
        game_world.add_collision_pair("player:homecar", None, home_car)
    else:
        if home_car and home_car.To_home:
            game_framework.change_mode(lobby_mode)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

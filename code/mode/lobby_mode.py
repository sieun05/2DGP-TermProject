from pico2d import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import game_framework
from . import play_mode, title_mode
from . import item_mode  # 추가: 아이템 모드로 전환
import game_world

from player2 import Player2
from zombie2 import Zombie2
import random
from container import Container
from lobby_car import Car
from player_ui import PlayerUI

def init():
    global image, player, zombies, container, car
    image = load_image('images/lobby.png')

    player = Player2()
    game_world.add_object(player, 1)

    zombies = [ Zombie2(random.randint(0, 1), random.randint(0, 3)) for _ in range(8) ]
    game_world.add_objects(zombies, 1)

    container = Container()
    game_world.add_object(container, 0)

    car = Car()
    game_world.add_object(car, 0)

    player_ui = PlayerUI()
    game_world.add_object(player_ui, 2)

def finish():
    game_world.clear()


def update():
    game_world.update()
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
    game_world.render()
    update_canvas()

#이벤트 변경해야함
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if container is not None:
                mx = event.x
                my = 600 - event.y
                # car 클릭인지 먼저 체크
                if car is not None:
                    c_left, c_bottom, c_right, c_top = car.get_bb()
                    if c_left <= mx <= c_right and c_bottom <= my <= c_top:
                        game_framework.change_mode(play_mode)
                        continue
                # container 클릭 체크
                left, bottom, right, top = container.get_bb()
                if left <= mx <= right and bottom <= my <= top:
                    game_framework.push_mode(item_mode)


def pause():
    pass


def resume():
    pass
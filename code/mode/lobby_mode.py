from pico2d import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import game_framework
from . import play_mode, title_mode
from player2 import Player2
from zombie2 import Zombie2
import random
from container import Container
from lobby_car import Car

image = None
player = None
zombies = []
container = None
car = None

def init():
    global image, player, zombies, container, car
    image = load_image('images/lobby.png')

    player = Player2()

    zombies = [ Zombie2(random.randint(0, 1), random.randint(0, 3)) for _ in range(8) ]

    container = Container()
    car = Car()

def finish():
    global image, player, zombies, container, car
    del player
    del image
    del zombies
    del container


def update():
    global player

    player.update()
    for zombie in zombies:
        zombie.update()
    pass


def draw():
    global image, player, zombies, container, car

    clear_canvas()
    image.draw(400, 300)
    player.draw()
    for zombie in zombies:
        zombie.draw()

    container.draw()
    car.draw()

    update_canvas()



#이벤트 변경해야함
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)


def pause():
    pass


def resume():
    pass
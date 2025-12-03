from pico2d import *
import sys
import os

import player

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import game_framework
from . import play_mode, title_mode
from Player2 import Player2

image = None
player = None

def init():
    global image, player
    image = load_image('images/lobby.png')

    player = Player2()


def finish():
    global image, player
    del player
    del image


def update():
    global player

    player.update()
    pass


def draw():
    global image, player

    clear_canvas()
    image.draw(400, 300)
    player.draw()
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
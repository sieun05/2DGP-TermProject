from pico2d import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import game_framework
from . import play_mode

image = None


def init():
    global image
    image = load_image('images/lobby.png')
    logo_start_time = get_time()


def finish():
    global image
    del image


def update():
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


#이벤트 변경해야함
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)


def pause():
    pass


def resume():
    pass
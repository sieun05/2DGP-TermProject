from pico2d import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import game_framework
from . import lobby_mode
import game_world
from item_select import SelectItem

image = None
image2 = None
select_item1, select_item2, select_item3 = None, None, None

def init():
    global image, image2, select_item1, select_item2, select_item3
    image = load_image('images/item.png')
    image2 = load_image('images/lobby.png')

    select_item1 = SelectItem(265, 330)
    select_item2 = SelectItem(400, 330)
    select_item3 = SelectItem(535, 330)

def finish():
    global image, image2, select_item1, select_item2, select_item3
    del image
    del image2
    del select_item1
    del select_item2
    del select_item3

def update():
    game_world.update()
    pass

def draw():
    clear_canvas()
    image2.draw(400,300)
    game_world.render()
    image.draw(400, 300)

    select_item1.draw()
    select_item2.draw()
    select_item3.draw()

    update_canvas()

#이벤트 변경해야함
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()


def pause():
    pass


def resume():
    pass
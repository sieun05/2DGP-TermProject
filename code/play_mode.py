from pico2d import *

import game_framework
import title_mode
from player import Player
# from grass import Grass
import game_world

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

    player = Player()
    game_world.add_object(player, 1)

    #
    # boy = Boy()
    # game_world.add_object(boy, 1)

    pass

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

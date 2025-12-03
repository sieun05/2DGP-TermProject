from pico2d import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import game_framework
from . import lobby_mode

image_back, image_pc, image_zom, image_font = None, None, None, None
timer_pc, timer_zom, timer_font = 0.0, 0.0, 0.0
pc_up, zom_up, font_up = True, True, True

image_pc_y, image_zom_y, image_font_y = 300, 300, 300

def init():
    global image_back, image_pc, image_zom, image_font
    image_back = load_image('images/title_back.png')
    image_pc = load_image('images/title_pc.png')
    image_zom = load_image('images/title_zom.png')
    image_font = load_image('images/title_font.png')
    logo_start_time = get_time()

    global timer_pc, timer_zom, timer_font
    timer_pc = timer_zom = timer_font = get_time()


def finish():
    global image_back, image_pc, image_zom, image_font
    del image_back, image_pc, image_zom, image_font

def update():
    global timer_pc, timer_zom, timer_font

    if get_time() - timer_pc > 0.05:
        timer_pc = get_time()

        global pc_up, image_pc_y
        if pc_up:
            image_pc_y += 1
            if image_pc_y >= 300:
                pc_up = False
        else:
            image_pc_y -= 1
            if image_pc_y <= 280:
                pc_up = True

    if get_time() - timer_zom > 0.05:
        timer_zom = get_time()

        global zom_up, image_zom_y
        if zom_up:
            image_zom_y += 2
            if image_zom_y >= 300:
                zom_up = False
        else:
            image_zom_y -= 2
            if image_zom_y <= 270:
                zom_up = True

    if get_time() - timer_font > 0.05:
        timer_font = get_time()

        global font_up, image_font_y
        if font_up:
            image_font_y += 1
            if image_font_y >= 320:
                font_up = False
        else:
            image_font_y -= 1
            if image_font_y <= 290:
                font_up = True

def draw():
    clear_canvas()

    image_back.draw(400, 300)
    image_pc.draw(400, image_pc_y)
    image_zom.draw(400, image_zom_y)
    image_font.draw(400, 300)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(lobby_mode)

def pause():
    pass

def resume():
    pass
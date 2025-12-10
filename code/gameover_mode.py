from pico2d import *

import game_framework
import title_mode
import common

image = None
font = None

def init():
    global image, font
    image = load_image('images/gameover.png')
    font = load_font('images/ENCR10B.TTF', 50)

def finish():
    global image, font
    del image, font

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    score = ((common.round + common.level) * 1000 +
             (common.player_max_heart + common.player_attack_power + common.player_attack_speed) * 20 +
             (common.apple + common.gear) * 10)
    font.draw(200, 250, f'score: {int(score)}', (0, 0, 0))
    update_canvas()

#이벤트 변경해야함
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass
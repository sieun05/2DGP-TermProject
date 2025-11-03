from pico2d import load_image, get_time
from sdl2 import *

import game_world
from state_machine import StateMachine

def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w
def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s
def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class Idle:
    def __init__(self, player):
        # player 인스턴스를 명시적으로 받아 참조하도록 수정
        self.player = player

    def enter(self, e):
        self.player.dir_x = 0
        self.player.dir_y = 0

    def exit(self, e):
        if space_down(e):
            self.player.attack()

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8

    def draw(self):
        # self.boy는 정의되어 있지 않아 경고/오류를 유발하므로 player 좌표로 변경
        if self.player.face_dir_x == 1:  # right
            self.player.image.clip_draw(self.player.frame * 100, 300, 100, 100, self.player.x, self.player.y)
        else:  # face_dir == -1: # left
            self.player.image.clip_draw(self.player.frame * 100, 200, 100, 100, self.player.x, self.player.y)


class Run:
    def __init__(self, player):
        # Run 상태도 player 인스턴스를 참조하도록 변경
        self.player = player

    def enter(self, e):
        if w_down(e):
            self.player.dir_y += 1
            self.player.face_dir_y = 1
        if s_down(e):
            self.player.dir_y -= 1
            self.player.face_dir_y = -1
        if a_down(e):
            self.player.dir_x -= 1
            self.player.face_dir_x = -1
        if d_down(e):
            self.player.dir_x += 1
            self.player.face_dir_x = 1

    def exit(self, e):
        if space_down(e):
            self.player.attack()

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8
        self.player.x += self.player.dir_x * 1
        self.player.y += self.player.dir_y * 1

    def draw(self):
        if self.player.face_dir_x == 1:  # right
            self.player.image.clip_draw(self.player.frame * 100, 100, 100, 100, self.player.x, self.player.y)
        else:  # face_dir == -1: # left
            self.player.image.clip_draw(self.player.frame * 100, 0, 100, 100, self.player.x, self.player.y)


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir_x = 1
        self.face_dir_y = 1
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('images/img.png')

        # 상태 객체 생성 시 현재 player 인스턴스를 전달
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {w_down: self.RUN, a_down: self.RUN, s_down: self.RUN, d_down: self.RUN, space_down: self.IDLE},
                self.RUN : {w_up: self.IDLE, a_up: self.IDLE, s_up: self.IDLE, d_up: self.IDLE,
                            w_down: self.RUN, a_down: self.RUN, s_down: self.RUN, d_down: self.RUN,
                            space_down: self.RUN},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()

    def attack(self):
        pass
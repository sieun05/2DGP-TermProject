from pico2d import load_image, get_time, load_font
from sdl2 import *

import game_world
from state_machine import StateMachine
from map import Map

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
        # 키 다운 이벤트에 따라 방향 값을 누적
        if w_down(e):
            self.player.dir_y += 1
            self.player.face_dir_y = 1
        elif s_down(e):
            self.player.dir_y -= 1
            self.player.face_dir_y = -1
        elif a_down(e):
            self.player.dir_x -= 1
            self.player.face_dir_x = -1
        elif d_down(e):
            self.player.dir_x += 1
            self.player.face_dir_x = 1

    def exit(self, e):
        # 키업 이벤트에 따라 방향 값을 감소
        if w_up(e):
            self.player.dir_y = self.player.dir_y - 1
        elif s_up(e):
            self.player.dir_y = self.player.dir_y + 1
        elif a_up(e):
            self.player.dir_x = self.player.dir_x + 1
        elif d_up(e):
            self.player.dir_x = self.player.dir_x - 1

        if space_down(e):
            self.player.attack()

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8

        if (self.player.map.x <= 0 or self.player.map.x >= 2400):

            if ((self.player.dir_x > 0 and self.player.map.x <= 0) or
                (self.player.dir_x < 0 and self.player.map.x >= 2400)):
                self.player.map.x += self.player.dir_x * 1
            else:
                self.player.x += self.player.dir_x * 1
        else:
            if ((self.player.dir_x > 0 and self.player.x <=400) or
                (self.player.dir_x < 0 and self.player.x >=400)):
                self.player.x += self.player.dir_x * 1
            else:
                self.player.map.x += self.player.dir_x * 1

            if self.player.map.x < 0:
                self.player.map.x = 0
            elif self.player.map.x > 2400:
                self.player.map.x = 2400

        if (self.player.map.y <= 0 or self.player.map.y >= 1800):

            if ((self.player.dir_y > 0 and self.player.map.y <= 0) or
                    (self.player.dir_y < 0 and self.player.map.y >= 1800)):
                self.player.map.y += self.player.dir_y * 1
            else:
                self.player.y += self.player.dir_y * 1
        else:
            if ((self.player.dir_y > 0 and self.player.y <= 300) or
                    (self.player.dir_y < 0 and self.player.y >= 300)):
                self.player.y += self.player.dir_y * 1
            else:
                self.player.map.y += self.player.dir_y * 1

            if self.player.map.y < 0:
                self.player.map.y = 0
            elif self.player.map.y > 1800:
                self.player.map.y = 1800

    def draw(self):
        if self.player.face_dir_x == 1:  # right
            self.player.image.clip_draw(self.player.frame * 100, 100, 100, 100, self.player.x, self.player.y)
        else:  # face_dir == -1: # left
            self.player.image.clip_draw(self.player.frame * 100, 0, 100, 100, self.player.x, self.player.y)


class Player:
    def __init__(self, map):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir_x = 1
        self.face_dir_y = 1
        self.dir_x = 0
        self.dir_y = 0
        self.map = map
        self.image = load_image('images/img.png')
        self.font = load_font('images/ENCR10B.TTF', 16)

        # 상태 객체 생성 시 현재 player 인스턴스를 전달
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {w_down: self.RUN, a_down: self.RUN, s_down: self.RUN, d_down: self.RUN, space_down: self.IDLE},
                self.RUN : {w_down: self.RUN, a_down: self.RUN, s_down: self.RUN, d_down: self.RUN,
                            w_up: self.RUN, a_up: self.RUN, s_up: self.RUN, d_up: self.RUN,
                            space_down: self.RUN},
            }
        )

    def update(self):
        self.state_machine.update()
        # RUN 상태에서 모든 방향키가 떼졌는지 확인하고 IDLE로 전환
        if self.state_machine.cur_state == self.RUN and self.dir_x == 0 and self.dir_y == 0:
            self.state_machine.cur_state = self.IDLE
            self.IDLE.enter(('STOP', None))

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 50, self.y + 50, f'({self.x}, {self.y})', (255, 255, 0))

    def attack(self):
        pass
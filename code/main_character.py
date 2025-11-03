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

class Idle:
    def __init__(self):
        pass

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Run:
    def __init__(self):
        pass

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Attack:
    def __init__(self):
        pass

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class Main_Character:
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('main_character.png')

        self.IDLE = Idle()
        self.RUN = Run()
        self.ATTACK = Attack()
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {w_down: self.RUN, a_down: self.RUN, s_down: self.RUN, d_down: self.RUN},
                self.RUN : {w_up: self.IDLE, a_up: self.IDLE, s_up: self.IDLE, d_up: self.IDLE},
                self.ATTACK : {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
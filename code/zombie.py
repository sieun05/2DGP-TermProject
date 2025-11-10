from pico2d import load_image, get_time, load_font
from sdl2 import *
import random

import game_world
from state_machine import StateMachine
from map import Map

class Idle:
    def __init__(self, zombie):
        self.zombie = zombie

    def enter(self, e):
        self.zombie.dir_x = 0
        self.zombie.dir_y = 0

    def exit(self, e):
        pass

    def do(self):
        self.zombie.frame = (self.zombie.frame + 1) % 8

    def draw(self):

        if (self.zombie.x - 400 < self.zombie.x and self.zombie.x + 400 > self.zombie.x and
            self.zombie.y - 300 < self.zombie.y and self.zombie.y + 300 > self.zombie.y):

            if self.zombie.face_dir_x == 1:  # right
                self.zombie.image.clip_draw(self.zombie.frame * 100, 300, 100, 100,
                                            self.zombie.x-(self.zombie.map.x-400), self.zombie.y-(self.zombie.map.y-300))
            else:  # face_dir == -1: # left
                self.zombie.image.clip_draw(self.zombie.frame * 100, 200, 100, 100,
                                            self.zombie.x-(self.zombie.map.x-400), self.zombie.y-(self.zombie.map.y-300))


class Zombie:
    def __init__(self, map):
        self.x, self.y = random.randint(0, 2400), random.randint(0, 1800)
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.face_dir_x = 1  # 기본적으로 오른쪽을 바라봄 (1: 오른쪽, -1: 왼쪽)
        self.map = map
        self.image = load_image('images/img.png')
        self.font = load_font('images/ENCR10B.TTF', 16)

        # 상태 객체 생성 시 현재 player 인스턴스를 전달
        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
            }
        )

    def update(self):
        self.state_machine.update()
        '''if self.dir_x == 0 and self.dir_y == 0:
            self.state_machine.cur_state = self.IDLE
            self.IDLE.enter(('STOP', None))'''

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-(self.map.x-400), self.y-(self.map.y-300), f'({self.x}, {self.y})', (255, 0, 0))

    def attack(self):
        pass

    def goto(self):
        pass
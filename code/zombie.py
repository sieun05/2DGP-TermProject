from pico2d import *
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
        self.zombie.frame = (self.zombie.frame + 1) % 4

    def draw(self):

        if (self.zombie.map.x - 100 < self.zombie.x and self.zombie.map.x + 900 > self.zombie.x and
            self.zombie.map.y - 100 < self.zombie.y and self.zombie.map.y + 700 > self.zombie.y):

            if self.zombie.face_dir_x == 1:  # right
                self.zombie.image.clip_draw(self.zombie.frame * 70, 910, 70, 70,
                                            self.zombie.x-(self.zombie.map.x), self.zombie.y-(self.zombie.map.y), 50, 50)
            else:  # face_dir == -1: # left
                self.zombie.image.clip_draw(self.zombie.frame * 70, 630, 70, 70,
                                            self.zombie.x-(self.zombie.map.x), self.zombie.y-(self.zombie.map.y), 50, 50)


class Zombie:
    def __init__(self, map):
        self.x, self.y = random.randint(0, 2400), random.randint(0, 1800)
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.face_dir_x = 1  # 기본적으로 오른쪽을 바라봄 (1: 오른쪽, -1: 왼쪽)
        self.map = map
        self.image = load_image('images/1.png')
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
        self.font.draw(self.x-(self.map.x), self.y-(self.map.y), f'({self.x}, {self.y})', (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def attack(self):
        pass

    def goto(self):
        pass

    def get_bb(self):
        return (self.x - (self.map.x) - 15, self.y - (self.map.y) - 15,
                self.x - (self.map.x) + 15, self.y - (self.map.y) + 15)

    # self.zombie.x - (self.zombie.map.x), self.zombie.y - (self.zombie.map.y)

    def handle_collisions(self, key, other):
        pass
from pico2d import *
from sdl2 import *
import game_framework

class Car:
    def __init__(self):
        self.x = 520
        self.y = 480

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def clear(self):
        pass

    def get_bb(self):
        return (self.x - 55, self.y - 60, self.x + 55, self.y + 60)

    def handle_collision(self, key, other):

        pass

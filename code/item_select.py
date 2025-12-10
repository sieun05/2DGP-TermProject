from pico2d import *
from sdl2 import *
import game_framework

class SelectItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def clear(self):
        pass

    def get_bb(self):
        return (self.x - 56, self.y - 64, self.x + 56, self.y + 64)

    def handle_collision(self, key, other):

        pass

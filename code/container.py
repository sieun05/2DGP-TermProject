from pico2d import *
from sdl2 import *
import game_framework

class Container:
    def __init__(self):
        self.x = 315
        self.y = 490

    def update(self):
        pass

    def draw(self):
        #draw_rectangle(*self.get_bb())
        pass

    def clear(self):
        pass

    def get_bb(self):
        return (self.x - 125, self.y - 85, self.x + 125, self.y + 85)

    def handle_collision(self, key, other):

        pass

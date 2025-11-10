from pico2d import *
from sdl2 import *

class Building:
    def __init__(self, map, x, y):
        self.image = load_image('images/building.png')
        self.font = load_font('images/ENCR10B.TTF', 16)
        self.x = x
        self.y = y
        self.map=map

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 160, 250, self.x-(self.map.x), self.y-(self.map.y)+125)
        self.font.draw(100, 400, f'({self.x}, {self.y})', (0, 0, 0))

    def clear(self):
        del self.image
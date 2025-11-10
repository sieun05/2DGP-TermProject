from pico2d import *
from sdl2 import *

class Map:
    def __init__(self):
        self.image = load_image('images/map.png')
        self.font = load_font('images/ENCR10B.TTF', 16)
        self.x = 400
        self.y = 300

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.x-400, self.y-300, 800, 600, 400, 300)
        self.font.draw(100, 500, f'({self.x}, {self.y})', (255, 255, 0))

    def clear(self):
        del self.image
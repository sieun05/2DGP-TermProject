from pico2d import *
from sdl2 import *
import game_framework
import common
import random

class Car3:
    def __init__(self, map, x, y):
        self.font = load_font('images/ENCR10B.TTF', 16)
        self.image = load_image('images/car3.png')
        self.x = x
        self.y = y
        self.map = map

        self.click_timer = 0.0
        self.To_home = False

    def update(self):
        if get_time() - self.click_timer >= 3.0:
            self.To_home = True

    def draw(self):
        self.image.clip_draw(0, 0, 97, 60, self.x - (self.map.x), self.y - (self.map.y), int(97*1.5), int(60*1.5))

    def clear(self):
        del self.image
        del self.font

    def get_bb(self):
        return (self.x - (self.map.x) - 90, self.y - (self.map.y) - 60,
                self.x - (self.map.x) + 90, self.y - (self.map.y) + 60)

    def handle_collision(self, key, other):
        pass

    def clicked(self):
        self.click_timer = get_time()

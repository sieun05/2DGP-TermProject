from pico2d import *
from sdl2 import *
import game_framework
import common
import random

class Car3:
    sound = None

    def __init__(self, map, x, y):
        self.font = load_font('images/ENCR10B.TTF', 16)
        self.image = load_image('images/car3.png')
        self.x = x
        self.y = y
        self.map = map

        self.click_timer = 0.0
        self.clicked_flag = False
        self.To_home = False

        if Car3.sound is None:
            Car3.sound = load_wav('sounds/car_horn.wav')
            Car3.sound.set_volume(64)

    def update(self):
        if self.clicked_flag and get_time() - self.click_timer >= 3.0:
            self.To_home = True

    def draw(self):
        self.image.clip_draw(0, 0, 97, 60, self.x - (self.map.x), self.y - (self.map.y), int(97*1.5), int(60*1.5))
        draw_rectangle(*self.get_bb())

    def clear(self):
        del self.image
        del self.font

    def get_bb(self):
        return (self.x - (self.map.x) - 90, self.y - (self.map.y) - 60,
                self.x - (self.map.x) + 90, self.y - (self.map.y) + 60)

    def handle_collision(self, key, other):
        pass

    def clicked(self):
        if self.clicked_flag == False:
            self.click_timer = get_time()
            self.clicked_flag = True
            Car3.sound.play()

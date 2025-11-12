from pico2d import *
from sdl2 import *

import game_world
import game_framework
from math import *

# gun Run Speed
PIXEL_PER_METER = (75.0 / 1.8)  # 75 pixel 1.8 meter
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Gun:
    def __init__(self, map, sx, sy, tx, ty):
        self.x, self.y = sx, sy
        self.sx, self.sy, self.tx, self.ty = sx, sy, tx, ty
        self.image = load_image('images/gun.png')
        self.map = map

        self.t = 0.0
        self.distance = math.sqrt((self.tx - self.x) ** 2 + (self.ty - self.y) ** 2)

    def update(self):
        if self.t < 1.0:
            self.t += RUN_SPEED_PPS * game_framework.frame_time / self.distance
            self.x = (1-self.t) * self.sx + self.t * self.tx
            self.y = (1-self.t) * self.sy + self.t * self.ty
        else:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x-(self.map.x), self.y-(self.map.y))
        draw_rectangle(*self.get_bb())

    def clear(self):
        del self.image

    def get_bb(self):
        return (self.x-(self.map.x) - 5, self.y-(self.map.y) - 5,
                self.x-(self.map.x) + 5, self.y-(self.map.y) + 5)

    def handle_collision(self, key, other):
        if key == "zombie:gun":
            game_world.remove_object(self)

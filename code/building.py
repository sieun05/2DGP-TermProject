from pico2d import *
from sdl2 import *
import game_framework
import common
import random

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Building:
    def __init__(self, map, x, y, num, check_flag):
        if num == 0:
            self.image = load_image('images/building.png')
        elif num == 1:
            self.image = load_image('images/building2.png')
        self.particle_image = load_image('images/particle.png')
        self.num_image = load_image('images/num.png')

        self.check_flag = False
        if check_flag == 1:
            self.check_flag = True

        self.font = load_font('images/ENCR10B.TTF', 16)
        self.x = x
        self.y = y
        self.map=map
        self.frame = 0

        self.explore_timer = 0.0
        self.explored = False

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if self.explored and get_time() - self.explore_timer > 5.0:
            self.explored = False
            common.apple += random.randint(0, 5)
            common.gear += random.randint(0, 5)

    def draw(self):
        self.image.clip_draw(0, 0, 160, 250, self.x-(self.map.x), self.y-(self.map.y)+125)
        if self.check_flag:
            self.particle_image.clip_draw(int(self.frame) * 160 , 0, 160, 119, self.x-(self.map.x), self.y-(self.map.y)+150)
        # self.font.draw(100, 400, f'({self.x}, {self.y})', (0, 0, 0))
        if self.explored:
            self.num_image.clip_draw((4-int(get_time()-self.explore_timer))*20, 0, 20, 20, self.x-(self.map.x), self.y-(self.map.y)+200, 40, 40)
        draw_rectangle(*self.get_bb())

    def clear(self):
        del self.image
        del self.particle_image

    def get_bb(self):
        return (self.x-(self.map.x) - 80, self.y-(self.map.y),
                self.x-(self.map.x) + 80, self.y-(self.map.y) + 100)

    # self.x-(self.map.x), self.y-(self.map.y)+125

    def explore(self):
        if self.check_flag == True:
            self.check_flag = False
            self.explored = True
            self.explore_timer = get_time()


    def handle_collision(self, key, other):
        # if key == "player:building":
        #     print(f"Player collided with Building at ({other.x}, {other.y})")
        # elif key == "player:zombie":
        #     print(f"Player collided with Zombie at ({other.x}, {other.y})")
        pass

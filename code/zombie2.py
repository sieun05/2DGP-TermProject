from pico2d import *
from sdl2 import *
import random

import game_framework  # 수정: from code import game_framework → import game_framework


# zombie Run Speed
PIXEL_PER_METER = (75.0 / 1.8)  # 75 pixel 1.8 meter
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

image = None

class Zombie2:
    def __init__(self, num, type):
        self.num = num

        if self.num == 0:
            self.x, self.y = random.randint(10, 140), random.randint(250, 600)
            self.tx, self.ty = random.randint(10, 140), random.randint(250, 600)
        else:
            self.x, self.y = random.randint(660, 790), random.randint(250, 600)
            self.tx, self.ty = random.randint(660, 790), random.randint(250, 600)

        self.frame = 0
        self.type = type

        global image
        if image == None:
            image = load_image('images/zombie.png')

        self.heart = 100

        # 인스턴스 변수로 속도 관리
        self.run_speed_pps = RUN_SPEED_PPS

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.dir = math.atan2(self.ty - self.y, self.tx - self.x)
        self.dir_x = self.tx - self.x
        distance = self.run_speed_pps * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

        distance_sq = (self.tx - self.x) ** 2 + (self.ty - self.y) ** 2
        if distance_sq < 0.5 * PIXEL_PER_METER ** 2:
            if self.num == 0:
                self.tx, self.ty = random.randint(10, 140), random.randint(250, 600)
            else:
                self.tx, self.ty = random.randint(660, 790), random.randint(250, 600)

    def handle_event(self, event):
        pass

    def draw(self):
        global image

        if self.dir_x > 0:  # right
            image.clip_draw(int(self.frame) * 256, 1024 + 256 * self.type, 256, 256, self.x, self.y, 90, 90)
        elif self.dir_x < 0:  # face_dir == -1: # left
            image.clip_draw(int(self.frame) * 256, 256 * self.type, 256, 256, self.x, self.y, 90, 90)


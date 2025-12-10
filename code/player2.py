from pico2d import *
from sdl2 import *
import random

import game_framework  # 수정: from code import game_framework → import game_framework


# player 속도
PIXEL_PER_METER = (75.0 / 1.8)  # 75 pixel 1.8 meter
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

# 발사율 설정: 20발/초
BULLETS_PER_SECOND = 20.0
BULLET_COOLDOWN = 1.0 / BULLETS_PER_SECOND

PLAYER_SIZE = 64

class Player2:
    def __init__(self):
        self.x, self.y = 400, 300
        self.tx, self.ty = random.randint(190, 610), random.randint(0, 400)
        self.frame = 0

        self.image = load_image('images/player.png')
        self.font = load_font('images/ENCR10B.TTF', 16)

        self.heart = 100
        self.dir_x = 0
        self.dir = 0

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
            self.tx, self.ty = random.randint(190, 610), random.randint(0, 400)

    def handle_event(self, event):
        pass

    def draw(self):
        if self.dir_x > 0:  # right
            self.image.clip_draw(int(self.frame) * 64, 64 * 5, 64, 64, int(self.x),
                                        int(self.y) + 30, PLAYER_SIZE, PLAYER_SIZE)
        elif self.dir_x < 0:  # face_dir == -1: # left
            self.image.clip_draw(int(self.frame) * 64, 64 * 6, 64, 64, int(self.x),
                                        int(self.y) + 30, PLAYER_SIZE, PLAYER_SIZE)


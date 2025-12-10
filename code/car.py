from pico2d import *
from sdl2 import *
import game_framework
import common
import random

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Car:
    def __init__(self, map, x, y, num, check_flag):
        if num == 0:
            self.image = load_image('images/car1.png')
        elif num == 1:
            self.image = load_image('images/car2.png')
        self.particle_image = load_image('images/particle.png')
        self.num_image = load_image('images/num.png')

        self.check_flag = True
        if check_flag == 1:
            self.check_flag = True

        self.font = load_font('images/ENCR10B.TTF', 16)
        self.x = x
        self.y = y
        self.map = map
        self.frame = 0

        # explore 관련 상태 (Building과 동일하게 동작)
        self.explore_timer = 0.0
        self.explored = False

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # 만약 explore 상태라면 일정 시간 후 해제 및 보상 추가 (Building과 동일)
        if self.explored and get_time() - self.explore_timer > 5.0:
            self.explored = False
            common.apple += random.randint(0, 5)
            common.gear += random.randint(0, 5)

    def draw(self):
        self.image.clip_draw(0, 0, 97, 60, self.x - (self.map.x), self.y - (self.map.y) + 30)
        if self.check_flag:
            self.particle_image.clip_draw(int(self.frame) * 160, 0, 160, 119, self.x - (self.map.x), self.y - (self.map.y) + 30)
        if self.explored:
            # Building과 동일한 방식으로 카운트 표시
            self.num_image.clip_draw((4 - int(get_time() - self.explore_timer)) * 20, 0, 20, 20,
                                     self.x - (self.map.x), self.y - (self.map.y) + 60, 40, 40)
        draw_rectangle(*self.get_bb())

    def clear(self):
        del self.image
        del self.particle_image
        del self.num_image

    def get_bb(self):
        return (self.x - (self.map.x) - 48, self.y - (self.map.y),
                self.x - (self.map.x) + 48, self.y - (self.map.y) + 30)

    def handle_collision(self, key, other):
        # 충돌 시 특별 처리 없음(플레이어가 밀려나지 않음). 플레이어는 player.handle_collision에서 처리
        pass

    def explore(self):
        # Building.explore과 동일한 동작
        if self.check_flag:
            self.check_flag = False
            self.explored = True
            self.explore_timer = get_time()

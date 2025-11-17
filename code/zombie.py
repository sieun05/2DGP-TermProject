from pico2d import *
from sdl2 import *
import random
import math

import game_world
import game_framework
from state_machine import StateMachine

# zombie Run Speed
PIXEL_PER_METER = (75.0 / 1.8)  # 75 pixel 1.8 meter
RUN_SPEED_KMPH = 13.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Idle:
    def __init__(self, zombie):
        self.zombie = zombie

    def enter(self, e):
        self.zombie.dir_x = 0
        self.zombie.dir_y = 0

    def exit(self, e):
        pass

    def do(self):
        self.zombie.frame = (self.zombie.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        old_x, old_y = self.zombie.x, self.zombie.y

        # 이동에 필요한 거리값이 0이면 division by zero 를 피하기 위해 처리
        if self.zombie.distance == 0:
            # 목표와 현재가 같으므로 이동 없음
            self.zombie.dir_x = 0
            self.zombie.dir_y = 0
            return

        if (self.zombie.t < 1.0 and
                (self.zombie.tx == self.zombie.player.x and self.zombie.ty == self.zombie.player.y)):
            self.zombie.t += RUN_SPEED_PPS * game_framework.frame_time / self.zombie.distance
            self.zombie.x = (1 - self.zombie.t) * self.zombie.sx + self.zombie.t * self.zombie.tx
            self.zombie.y = (1 - self.zombie.t) * self.zombie.sy + self.zombie.t * self.zombie.ty
        else:
            self.zombie.sx, self.zombie.sy = self.zombie.x, self.zombie.y
            self.zombie.tx, self.zombie.ty = self.zombie.player.x, self.zombie.player.y
            self.zombie.t = 0.0
            self.zombie.distance = math.sqrt((self.zombie.tx - self.zombie.x) ** 2 + (self.zombie.ty - self.zombie.y) ** 2)

            # distance가 0이면 더 이상 이동할 필요 없음
            if self.zombie.distance == 0:
                self.zombie.dir_x = 0
                self.zombie.dir_y = 0
                return

            self.zombie.t += RUN_SPEED_PPS * game_framework.frame_time / self.zombie.distance
            self.zombie.x = (1 - self.zombie.t) * self.zombie.sx + self.zombie.t * self.zombie.tx
            self.zombie.y = (1 - self.zombie.t) * self.zombie.sy + self.zombie.t * self.zombie.ty

        if ((1 - self.zombie.t) * self.zombie.sx + self.zombie.t * self.zombie.tx) - old_x > 0:
            self.zombie.dir_x = 1
        elif ((1 - self.zombie.t) * self.zombie.sx + self.zombie.t * self.zombie.tx) - old_x < 0:
            self.zombie.dir_x = -1
        else:
            self.zombie.dir_x = 0

        if ((1 - self.zombie.t) * self.zombie.sy + self.zombie.t * self.zombie.ty) - old_y > 0:
            self.zombie.dir_y = 1
        elif ((1 - self.zombie.t) * self.zombie.sy + self.zombie.t * self.zombie.ty) - old_y < 0:
            self.zombie.dir_y = -1
        else:
            self.zombie.dir_y = 0

    def draw(self):

        if (self.zombie.map.x - 100 < self.zombie.x and self.zombie.map.x + 900 > self.zombie.x and
            self.zombie.map.y - 100 < self.zombie.y and self.zombie.map.y + 700 > self.zombie.y):

            if self.zombie.dir_x == 1:  # right
                self.zombie.image.clip_draw(int(self.zombie.frame) * 70, 910, 70, 70,
                                            self.zombie.x-(self.zombie.map.x), self.zombie.y-(self.zombie.map.y), 50, 50)
            else:  # face_dir == -1: # left
                self.zombie.image.clip_draw(int(self.zombie.frame) * 70, 630, 70, 70,
                                            self.zombie.x-(self.zombie.map.x), self.zombie.y-(self.zombie.map.y), 50, 50)


class Zombie:
    def __init__(self, map, player):
        self.x, self.y = random.randint(0, 2400), random.randint(0, 1800)
        self.frame = 0
        self.dir_x = 1  # 기본적으로 오른쪽을 바라봄 (1: 오른쪽, -1: 왼쪽)
        self.dir_y = 1  # 기본적으로 오른쪽을 바라봄 (1: 오른쪽, -1: 왼쪽)
        self.map = map
        self.player = player
        self.image = load_image('images/1.png')
        self.font = load_font('images/ENCR10B.TTF', 16)

        self.heart = 100

        self.t=0.0
        self.sx, self.sy = self.x, self.y       # start x, y
        self.tx, self.ty = self.player.x, self.player.y       # target

        self.distance = math.sqrt((self.tx - self.x) ** 2 + (self.ty - self.y) ** 2)

        # 상태 객체 생성 시 현재 player 인스턴스를 전달
        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
            }
        )

    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-(self.map.x), self.y-(self.map.y), f'({self.heart})', (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def attack(self):
        pass

    def goto(self):
        pass

    def get_bb(self):
        return (self.x - (self.map.x) - 15, self.y - (self.map.y) - 15,
                self.x - (self.map.x) + 15, self.y - (self.map.y) + 15)

    # self.zombie.x - (self.zombie.map.x), self.zombie.y - (self.zombie.map.y)

    def handle_collision(self, key, other):
        if key == "player:zombie":
            pass
        elif key == "zombie:building":
            # World 좌표 기준으로 바운딩 박스 계산
            left_a = self.x - 15
            bottom_a = self.y - 15
            right_a = self.x + 15
            top_a = self.y + 15

            left_b = other.x - 80
            bottom_b = other.y
            right_b = other.x + 80
            top_b = other.y + 100

            overlap_x = min(right_a, right_b) - max(left_a, left_b)
            overlap_y = min(top_a, top_b) - max(bottom_a, bottom_b)

            if overlap_x > 0 and overlap_y > 0:
                # 더 적게 겹친 축으로 분리
                if overlap_x < overlap_y:
                    # x축으로 분리: 건물 왼쪽/오른쪽으로 배치
                    if self.x < other.x:
                        self.x = left_b - 15
                    else:
                        self.x = right_b + 15
                    # x는 고정하고 y축으로만 플레이어 쪽으로 이동시키기 위해 목표 설정
                    self.sx, self.sy = self.x, self.y
                    self.tx, self.ty = self.x, self.player.y
                else:
                    # y축으로 분리: 건물 아래/위로 배치
                    if self.y < other.y:
                        self.y = bottom_b - 15
                    else:
                        self.y = top_b + 15
                    # y는 고정하고 x축으로만 플레이어 쪽으로 이동시키기 위해 목표 설정
                    self.sx, self.sy = self.x, self.y
                    self.tx, self.ty = self.player.x, self.y

                # 이동 파라미터 재설정
                self.t = 0.0
                self.distance = math.sqrt((self.tx - self.x) ** 2 + (self.ty - self.y) ** 2)

                if self.distance == 0:
                    self.dir_x = 0
                    self.dir_y = 0
                else:
                    dx = self.tx - self.x
                    dy = self.ty - self.y
                    self.dir_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
                    self.dir_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
        elif key == "zombie:zombie":
            if self.x < other.x:
                self.x -= 0.2
            if self.y < other.y:
                self.y -= 0.2
            # print(f"Zombie collided with Zombie at ({other.x}, {other.y})")
        elif key == "zombie:gun":
            self.heart -= 5

            if self.heart <= 0:
                game_world.remove_object(self)
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
                Zombie.zombie_image.clip_draw(int(self.zombie.frame) * 70, 910, 70, 70,
                                            self.zombie.x-(self.zombie.map.x), self.zombie.y-(self.zombie.map.y), 50, 50)
            else:  # face_dir == -1: # left
                Zombie.zombie_image.clip_draw(int(self.zombie.frame) * 70, 630, 70, 70,
                                            self.zombie.x-(self.zombie.map.x), self.zombie.y-(self.zombie.map.y), 50, 50)


class Zombie:
    # 클래스 변수: 모든 좀비 인스턴스가 공유
    zombie_image = None
    zombie_font = None

    @classmethod
    def load_resources(cls):
        """클래스 리소스를 로드 (한 번만 실행)"""
        if cls.zombie_image is None:
            cls.zombie_image = load_image('images/1.png')
        if cls.zombie_font is None:
            cls.zombie_font = load_font('images/ENCR10B.TTF', 16)

    def __init__(self, map, player, x=None, y=None):
        # 클래스 리소스 로드 (처음 호출시에만 실제로 로드됨)
        Zombie.load_resources()

        # 위치 설정 (x, y가 주어지지 않으면 랜덤)
        if x is None or y is None:
            self.x, self.y = random.randint(0, 2400), random.randint(0, 1800)
        else:
            self.x, self.y = x, y

        self.frame = 0
        self.dir_x = 1  # 기본적으로 오른쪽을 바라봄 (1: 오른쪽, -1: 왼쪽)
        self.dir_y = 1  # 기본적으로 오른쪽을 바라봄 (1: 오른쪽, -1: 왼쪽)
        self.map = map
        self.player = player

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
        self.zombie_font.draw(self.x-(self.map.x), self.y-(self.map.y), f'({self.heart})', (255, 0, 0))
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
                else:
                    # y축으로 분리: 건물 아래/위로 배치
                    if self.y < other.y:
                        self.y = bottom_b - 15
                    else:
                        self.y = top_b + 15

                # 충돌 후 새로운 경로 설정: 항상 플레이어를 향하도록 함
                self.sx, self.sy = self.x, self.y
                self.tx, self.ty = self.player.x, self.player.y
                self.t = 0.0
                self.distance = math.sqrt((self.tx - self.x) ** 2 + (self.ty - self.y) ** 2)

                # 방향 업데이트
                if self.distance > 0:
                    dx = self.tx - self.x
                    dy = self.ty - self.y
                    self.dir_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
                    self.dir_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
                else:
                    self.dir_x = 0
                    self.dir_y = 0
        elif key == "zombie:zombie":
            # 두 좀비 간의 거리 벡터 계산
            dx = self.x - other.x
            dy = self.y - other.y

            # 완전히 같은 위치에 있는 경우 랜덤 방향으로 아주 조금 이동
            if dx == 0 and dy == 0:
                angle = random.uniform(0, 2 * math.pi)
                dx = math.cos(angle) * 0.1
                dy = math.sin(angle) * 0.1

            # 거리 계산
            distance = math.sqrt(dx * dx + dy * dy)

            # 바운딩 박스가 실제로 겹치는지만 체크 (반지름 15씩)
            if distance < 30 and distance > 0:  # 15 + 15 = 30
                # 정규화된 방향 벡터
                nx = dx / distance
                ny = dy / distance

                # 매우 작은 힘으로만 밀어냄 (자연스러운 움직임)
                push_force = 0.15  # 0.1~0.2 범위의 작은 힘

                # 현재 좀비를 아주 조금 밀어냄
                self.x += nx * push_force
                self.y += ny * push_force
        elif key == "zombie:gun":
            self.heart -= 5

            if self.heart <= 0:
                game_world.remove_object(self)
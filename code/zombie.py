from pico2d import *
from sdl2 import *
import random

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
        self.zombie.frame = (self.zombie.frame + 1) % 4
        old_x, old_y = self.zombie.x, self.zombie.y

        if (self.zombie.t < 1.0 and
                (self.zombie.tx == self.zombie.player.x and self.zombie.ty == self.zombie.player.y)):
            self.zombie.t += RUN_SPEED_PPS * game_framework.frame_time / self.zombie.distance
            self.zombie.x = (1-self.zombie.t) * self.zombie.sx + self.zombie.t * self.zombie.tx
            self.zombie.y = (1-self.zombie.t) * self.zombie.sy + self.zombie.t * self.zombie.ty
        else:
            self.zombie.sx, self.zombie.sy = self.zombie.x, self.zombie.y
            self.zombie.tx, self.zombie.ty = self.zombie.player.x, self.zombie.player.y
            self.zombie.t = 0.0
            self.zombie.distance = math.sqrt((self.zombie.tx - self.zombie.x) ** 2 + (self.zombie.ty - self.zombie.y) ** 2)

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
                self.zombie.image.clip_draw(self.zombie.frame * 70, 910, 70, 70,
                                            self.zombie.x-(self.zombie.map.x), self.zombie.y-(self.zombie.map.y), 50, 50)
            else:  # face_dir == -1: # left
                self.zombie.image.clip_draw(self.zombie.frame * 70, 630, 70, 70,
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
            if self.x + 15 >= (other.x - 80) or self.x - 15 <= (other.x + 80):
                self.x -= self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
            if self.y + 15 >= (other.y) or self.y - 15 <= (other.y + 100):
                self.y -= self.dir_y * RUN_SPEED_PPS * game_framework.frame_time
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
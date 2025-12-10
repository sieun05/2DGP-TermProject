from pico2d import *
from sdl2 import *

import common
import game_world
import game_framework  # 수정: from code import game_framework → import game_framework
from state_machine import StateMachine
from map import Map
from gun import Gun
from zombie import Zombie

def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w
def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s
def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

# player 속도
PIXEL_PER_METER = (75.0 / 1.8)  # 75 pixel 1.8 meter
RUN_SPEED_KMPH = 15.0  # Km / Hour
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


class Idle:
    def __init__(self, player):
        # player 인스턴스를 명시적으로 받아 참조하도록 수정
        self.player = player

    def enter(self, e):
        self.player.dir_x = 0
        self.player.dir_y = 0

    def exit(self, e):
        if space_down(e) and self.player.building_crash_flag:
            self.player.building_check()
        if space_down(e) and self.player.crash_car is not None:
            self.player.building_check()

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        if self.player.damage_flag:
            frame_y_sub = 4
        else:
            frame_y_sub = 0

        if self.player.face_dir_x == 1:  # right
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (5 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE, PLAYER_SIZE)
        elif self.player.face_dir_x == -1:  # face_dir == -1: # left
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (6 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE,PLAYER_SIZE)
        elif self.player.face_dir_y == -1:  # up
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (7 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE, PLAYER_SIZE)
        else:  # face_dir == -1: # down
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (4 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE, PLAYER_SIZE)

class Run:
    def __init__(self, player):
        # Run 상태도 player 인스턴스를 참조하도록 변경
        self.player = player

    def enter(self, e):
        # 키 다운 이벤트에 따라 방향 값을 누적
        if w_down(e):
            self.player.dir_y += 1
            self.player.face_dir_y = 1
        elif s_down(e):
            self.player.dir_y -= 1
            self.player.face_dir_y = -1
        elif a_down(e):
            self.player.dir_x -= 1
            self.player.face_dir_x = -1
        elif d_down(e):
            self.player.dir_x += 1
            self.player.face_dir_x = 1

    def exit(self, e):
        self.player.face_dir_x = self.player.dir_x
        self.player.face_dir_y = self.player.dir_y

        # 키업 이벤트에 따라 방향 값을 감소
        if w_up(e):
            self.player.dir_y = self.player.dir_y - 1
        elif s_up(e):
            self.player.dir_y = self.player.dir_y + 1
        elif a_up(e):
            self.player.dir_x = self.player.dir_x + 1
        elif d_up(e):
            self.player.dir_x = self.player.dir_x - 1

        if space_down(e) and self.player.building_crash_flag:
            self.player.building_check()



    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

         # 이동 거리 계산
        dis_x = self.player.dir_x * self.player.run_speed_pps * game_framework.frame_time
        dis_y = self.player.dir_y * self.player.run_speed_pps * game_framework.frame_time

        new_x = self.player.w_x
        new_y = self.player.w_y
        new_map_x = self.player.map.x
        new_map_y = self.player.map.y

        if (self.player.map.x <= 0 or self.player.map.x >= 2400 - 800):
            if ((self.player.dir_x > 0 and self.player.map.x <= 0) or
                (self.player.dir_x < 0 and self.player.map.x >= 2400 - 800)):
                self.player.map.x += dis_x
            else:
                self.player.w_x += dis_x
        else:
            if ((self.player.dir_x > 0 and self.player.w_x <=400) or
                (self.player.dir_x < 0 and self.player.w_x >=400)):
                self.player.w_x += dis_x
            else:
                self.player.map.x += dis_x

            if self.player.map.x < 0:
                self.player.map.x = 0
            elif self.player.map.x > 2400 - 800:
                self.player.map.x = 2400 - 800


        if (self.player.map.y <= 0 or self.player.map.y >= 1800 - 600):

            if ((self.player.dir_y > 0 and self.player.map.y <= 0) or
                    (self.player.dir_y < 0 and self.player.map.y >= 1800 - 600)):
                self.player.map.y += dis_y
            else:
                self.player.w_y += dis_y
        else:
            if ((self.player.dir_y > 0 and self.player.w_y <= 300) or
                    (self.player.dir_y < 0 and self.player.w_y >= 300)):
                self.player.w_y += dis_y
            else:
                self.player.map.y += dis_y

            if self.player.map.y < 0:
                self.player.map.y = 0
            elif self.player.map.y > 1800 - 600:
                self.player.map.y = 1800 - 600

        if self.player.w_x < 0:
            self.player.w_x = 0
        elif self.player.w_x > 800:
            self.player.w_x = 800
        if self.player.w_y < 0:
            self.player.w_y = 0
        elif self.player.w_y > 600:
            self.player.w_y = 600

    def draw(self):
        if self.player.damage_flag:
            frame_y_sub = 4
        else:
            frame_y_sub = 0

        if self.player.dir_x == 1:  # right
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (5 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE, PLAYER_SIZE)
        elif self.player.dir_x == -1:  # face_dir == -1: # left
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (6 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE, PLAYER_SIZE)
        elif self.player.dir_y == -1:  # up
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (7 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE, PLAYER_SIZE)
        else:  # face_dir == -1: # down
            self.player.image.clip_draw(int(self.player.frame) * 64, 64 * (4 - frame_y_sub), 64, 64, int(self.player.w_x),
                                        int(self.player.w_y) + 30, PLAYER_SIZE, PLAYER_SIZE)

class Player:
    def __init__(self, map):
        self.w_x, self.w_y = 400, 300
        self.face_dir_x, self.face_dir_y = 1, 1
        self.dir_x, self.dir_y = 0, 0
        self.frame = 0

        self.building_crash_flag = False
        self.crash_building = None
        self.crash_car = None

        self.gun_tx = 0
        self.gun_ty = 0

        self.map = map
        self.image = load_image('images/player.png')
        self.font = load_font('images/ENCR10B.TTF', 16)

        self.x, self.y = self.w_x+ self.map.x, self.w_y +self.map.y

        self.damage_flag = False
        self.damage_time = 0.0
        self.heart = 10
        self.heart_delay_timer = 0.0
        self.heart_delay_flag = True

        self.gun_delay_timer = 0.0  # get_time() 대신 0.0으로 초기화

        # 인스턴스 변수로 속도 관리
        self.run_speed_pps = RUN_SPEED_PPS

        # 게임오버 푸시 플래그 초기화 (안전성 보장)
        self.gameover_pushed = False

        # 상태 객체 생성 시 현재 player 인스턴스를 전달
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {w_down: self.RUN, a_down: self.RUN, s_down: self.RUN, d_down: self.RUN, space_down: self.IDLE},
                self.RUN : {w_down: self.RUN, a_down: self.RUN, s_down: self.RUN, d_down: self.RUN,
                            w_up: self.RUN, a_up: self.RUN, s_up: self.RUN, d_up: self.RUN,
                            space_down: self.RUN},
            }
        )

    def update(self):
        self.x, self.y = self.w_x + self.map.x, self.w_y + self.map.y

        self.state_machine.update()


        # RUN 상태에서 모든 방향키가 떼졌는지 확인하고 IDLE로 전환
        if self.state_machine.cur_state == self.RUN and self.dir_x == 0 and self.dir_y == 0:
            self.state_machine.cur_state = self.IDLE
            self.IDLE.enter(('STOP', None))

        # 총알 발사 딜레이 관리
        BULLET_COOLDOWN = 1.0 / common.player_attack_speed

        self.gun_delay_timer += game_framework.frame_time
        if self.gun_delay_timer >= BULLET_COOLDOWN:
            self.gun_delay_timer = 0.0  # 타이머를 0으로 리셋
            gun = Gun(self.map, self.x + self.face_dir_x * 5, self.y + 25, self.gun_tx, self.gun_ty)
            game_world.add_object(gun, 1)
            game_world.add_collision_pair("zombie:gun", None, gun)

        # 데미지 상태 관리 (속도 감소 효과)
        if self.damage_flag:
            self.damage_time += game_framework.frame_time
            if self.damage_time >= 3:
                self.damage_flag = False
                run_speed_kmph = 15.0  # Km / Hour
                run_speed_mpm = (run_speed_kmph * 1000.0 / 60.0)
                run_speed_mps = (run_speed_mpm / 60.0)
                self.run_speed_pps = (run_speed_mps * PIXEL_PER_METER)
            else:
                run_speed_kmph = 13.0  # Km / Hour
                run_speed_mpm = (run_speed_kmph * 1000.0 / 60.0)
                run_speed_mps = (run_speed_mpm / 60.0)
                self.run_speed_pps = (run_speed_mps * PIXEL_PER_METER)

        # HP 감소 딜레이 관리: 0.5초마다 heart_delay_flag를 True로 재설정
        self.heart_delay_timer += game_framework.frame_time
        if self.heart_delay_timer >= 0.5:
            self.heart_delay_flag = True

        # 건물과의 상호작용 거리 체크 (충돌 처리 후에 실행)
        self.check_building_interaction()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

        # print(f"Mouse x, y at ({event.x}, {event.y})")

        if event.x is not None and event.y is not None:
            self.gun_tx = event.x + self.map.x
            self.gun_ty = (600-event.y) + self.map.y

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.w_x - 50, self.w_y + 50, f'(heart: {self.heart})', (0, 0, 0))
        draw_rectangle(*self.get_bb())

    def building_check(self):
        if self.crash_building is not None:
            self.crash_building.explore()
            self.crash_building = None
        if self.crash_car is not None:
            # 먼저 explore 호출하고, 이후에 참조를 해제합니다.
            try:
                self.crash_car.explore()
                print("Car explored")
            except Exception:
                pass
            self.crash_car = None

    def check_building_interaction(self):
        """건물과의 상호작용 가능한 거리인지 체크"""
        self.building_crash_flag = False  # 기본값은 False

        # game_world에서 모든 건물 객체를 가져와서 거리 체크
        for layer in game_world.world:
            for obj in layer:
                # Building 클래스의 객체인지 확인 (타입 체크)
                if obj.__class__.__name__ == 'Building':
                    # 플레이어와 건물 간의 거리 계산
                    distance_x = abs(self.x - obj.x)
                    distance_y = abs(self.y - (obj.y + 40))  # 건물 중심 높이 보정

                    # 상호작용 가능한 거리 (건물 바운딩박스보다 약간 큰 범위)
                    # 건물 바운딩박스: x축 ±80, y축 0~100
                    interaction_distance_x = 100  # 80 + 20 (여유 거리)
                    interaction_distance_y = 70  # 100 + 20 (여유 거리)

                    if distance_x <= interaction_distance_x and distance_y <= interaction_distance_y:
                        self.building_crash_flag = True
                        return

    def get_bb(self):   # 충돌체크용 바운딩 박스, left, bottom, right, top 순서로 반환
        return self.w_x - 10, self.w_y - 5, self.w_x + 10, self.w_y + 20

    def handle_collision(self, key, other):
        if key == "player:building":

            if self.x + 10 >= (other.x - 80) or self.x - 10 <= (other.x + 80):
                self.w_x -= 2 * self.dir_x * self.run_speed_pps * game_framework.frame_time
            if self.y + 5 >= (other.y) or self.y - 20 <= (other.y + 100):
                self.w_y -= 2 * self.dir_y * self.run_speed_pps * game_framework.frame_time

            self.building_crash_flag = True
            self.crash_building = other

        elif key == "player:car":
            # car와 겹쳐도 플레이어를 밀어내지 않음.
            # 스페이스바로 상호작용할 수 있도록 플래그를 세우고 충돌 대상을 저장합니다.
            self.building_crash_flag = True
            self.crash_car = other

        elif key == "player:zombie":
            self.damage_flag = True
            self.damage_time = 0.0

            if self.heart_delay_flag:
                self.heart_delay_flag = False
                self.heart_delay_timer = 0.0  # frame_time 기반 누적 타이머로 변경
                common.player_heart -= 3  # HP 감소 코드 추가

            # gameover 판단 및 push는 play_mode에서 처리합니다.

    def reset(self):
        """플레이어 상태를 초기값으로 리셋"""
        self.w_x, self.w_y = 400, 300
        self.face_dir_x, self.face_dir_y = 1, 1
        self.dir_x, self.dir_y = 0, 0
        self.frame = 0

        self.building_crash_flag = False

        self.damage_flag = False
        self.damage_time = 0.0
        self.heart = 100
        self.heart_delay_timer = 0.0
        self.heart_delay_flag = True

        self.gun_delay_timer = 0.0  # get_time() 대신 0.0으로 초기화

        # 속도도 초기값으로 리셋
        self.run_speed_pps = RUN_SPEED_PPS

        # 상태 머신을 IDLE로 초기화
        self.state_machine.cur_state = self.IDLE
        self.IDLE.enter(('START', None))

    def attack(self):
        pass

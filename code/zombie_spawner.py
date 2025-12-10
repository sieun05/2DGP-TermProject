from pico2d import *
import game_framework
import game_world
from zombie import Zombie
import random
import math

class ZombieSpawner:
    def __init__(self, round, x, y, map, player):
        self.round = round
        self.x = x
        self.y = y
        self.map = map
        self.player = player

        # ===== 튜닝 포인트(여기만 수정하면 좀비 생성 수/빈도 조절 가능) =====
        # base_spawn_interval: 기본 소환 간격(초). 값이 작을수록 자주 소환됩니다.
        self.base_spawn_interval = 5.0
        # base_spawn_count: 기본 한 번 소환당 생성 수. 증가시키면 한 번에 더 많은 좀비가 등장합니다.
        self.base_spawn_count = 1
        # min_spawn_interval: 소환 간격의 최소값(클램프). 너무 작게 내려가지 않도록 제한합니다.
        self.min_spawn_interval = 0.3
        # max_total_zombies: 월드에 존재할 수 있는 전체 좀비 상한(성능/밸런스 목적).
        self.max_total_zombies = 10 + (round - 1) * 5
        # ===================================================================

        # 동적 상태 (보통 조정 불필요)
        self.spawn_interval = self.base_spawn_interval
        self.spawn_count = self.base_spawn_count
        self.spawn_timer = 0.0
        self.spawn_cooldown = self.spawn_interval
        self.total_time = 0.0

        self.active = True

        # 내부 caps: 라운드 기반 최대 한 번에 소환 개수
        self.max_spawn_count = max(3, 6)

    def update(self):
        if not self.active:
            return

        total_zombies = len(game_world.get_objects_by_type(Zombie))
        if total_zombies >= self.max_total_zombies:
            return

        # 누적 시간 증가
        self.total_time += game_framework.frame_time

        # ===== 동적 증가 로직(원하면 수정 가능) =====
        # 시간이 지날수록 spawn_interval을 선형으로 감소시켜 소환 빈도를 높입니다.
        # - 계수(0.05)를 조절하면 감소 속도를 바꿀 수 있습니다.
        # spawn_count는 10초마다 1씩 증가하도록 되어 있습니다.
        # - //10 대신 다른 값으로 변경하면 증가 주기를 바꿀 수 있습니다.
        self.spawn_interval = max(self.min_spawn_interval, self.base_spawn_interval - self.total_time * 0.05)
        self.spawn_count = min(self.max_spawn_count, self.base_spawn_count + int(self.total_time // 10))
        # ==================================================

        self.spawn_timer += game_framework.frame_time
        if self.spawn_timer >= self.spawn_cooldown:
            self.spawn_zombies()
            self.spawn_timer = 0.0
            variation = random.uniform(-0.2, 0.2)
            self.spawn_cooldown = max(self.min_spawn_interval, self.spawn_interval + variation)

    def spawn_zombies(self):
        total_zombies = len(game_world.get_objects_by_type(Zombie))
        if total_zombies >= self.max_total_zombies:
            return

        # 이번에 생성할 좀비 수: 남은 허용량과 spawn_count 중 작은 값을 선택
        zombies_to_spawn = min(self.spawn_count, self.max_total_zombies - total_zombies)
        if zombies_to_spawn <= 0:
            return

        existing_zombies = game_world.get_objects_by_type(Zombie)
        newly_spawned = []

        for i in range(zombies_to_spawn):
            spawn_radius = 50 + i * 20
            angle = random.uniform(0, 2 * math.pi)
            spawn_x = self.x + math.cos(angle) * spawn_radius
            spawn_y = self.y + math.sin(angle) * spawn_radius
            spawn_x = max(50, min(2350, spawn_x))
            spawn_y = max(50, min(1750, spawn_y))
            zombie_type = random.randint(0, 3)

            zombie = Zombie(self.map, self.player, zombie_type, spawn_x, spawn_y)
            game_world.add_object(zombie, 1)
            newly_spawned.append(zombie)

        for zombie in newly_spawned:
            game_world.add_collision_pair("player:zombie", None, zombie)
            game_world.add_collision_pair("zombie:building", zombie, None)
            game_world.add_collision_pair("zombie:gun", zombie, None)

        for i, new_zombie in enumerate(newly_spawned):
            for existing_zombie in existing_zombies:
                game_world.add_collision_pair("zombie:zombie", new_zombie, existing_zombie)
            for j in range(i + 1, len(newly_spawned)):
                other_new_zombie = newly_spawned[j]
                game_world.add_collision_pair("zombie:zombie", new_zombie, other_new_zombie)

        # 디버그 로그: 원치 않으면 이 print를 삭제하세요.
        print(f"Spawner({self.x:.0f},{self.y:.0f}) spawned {len(newly_spawned)} zombies. total_time={self.total_time:.1f}s, interval={self.spawn_interval:.2f}s, count={self.spawn_count}")

    def draw(self):
        pass

    def clear(self):
        # 비활성화 및 타이머 초기화
        self.active = False
        self.spawn_timer = 0.0
        self.spawn_cooldown = self.spawn_interval
        self.total_time = 0.0

    def get_bb(self):
        pass

    def handle_collision(self, key, other):
        pass

    def set_active(self, active):
        self.active = active

    def reset_for_new_round(self, new_round):
        self.round = new_round
        self.current_spawn_count = 0
        # 라운드에 따라 기본값 조정(필요하면 여기도 조절)
        self.base_spawn_interval = max(0.5, 5.0 - (new_round - 1) * 0.3)
        self.base_spawn_count = max(1, 1 + (new_round - 1) // 2)
        self.max_spawn_count = max(6, 3 + new_round)
        self.spawn_timer = 0.0
        self.spawn_cooldown = self.base_spawn_interval
        self.total_time = 0.0

    def reset(self):
        self.round = 1
        self.spawn_interval = self.base_spawn_interval
        self.spawn_count = self.base_spawn_count
        self.spawn_timer = 0.0
        self.spawn_cooldown = self.spawn_interval
        self.total_time = 0.0
        self.active = True

from pico2d import *
from sdl2 import *
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

        # 라운드에 따른 스포너 설정 - 임시로 5초당 1마리로 조정
        self.base_spawn_interval = 5.0  # 5초 간격으로 변경
        self.base_spawn_count = 1       # 기본 소환 개수

        # 임시로 라운드 증가 효과 비활성화
        self.spawn_interval = self.base_spawn_interval  # 라운드와 무관하게 5초 고정
        self.spawn_count = self.base_spawn_count        # 라운드와 무관하게 1마리 고정

        # 타이머
        self.spawn_timer = 0.0
        self.spawn_cooldown = self.spawn_interval

        # 스포너 활성화 여부
        self.active = True

        # 라운드당 최대 소환 수도 줄임
        self.max_spawns_per_round = 3 + round  # 누락된 속성 추가
        self.current_spawn_count = 0

    def update(self):
        if not self.active or self.current_spawn_count >= self.max_spawns_per_round:
            return

        # 전체 좀비 수 체크 - 10마리가 되면 생성 중지
        total_zombies = len(game_world.get_objects_by_type(Zombie))
        if total_zombies >= 20:
            return

        # 소환 타이머 업데이트
        self.spawn_timer += game_framework.frame_time

        # 소환 시간이 되었는지 확인
        if self.spawn_timer >= self.spawn_cooldown:
            self.spawn_zombies()
            self.spawn_timer = 0.0

            # 다음 소환까지의 시간을 약간 랜덤하게 조정
            variation = random.uniform(-0.2, 0.2)
            self.spawn_cooldown = max(0.3, self.spawn_interval + variation)

    def spawn_zombies(self):
        """좀비들을 소환"""
        if self.current_spawn_count >= self.max_spawns_per_round:
            return

        # 전체 좀비 수 체크 - 10마리가 되면 생성 중지
        total_zombies = len(game_world.get_objects_by_type(Zombie))
        if total_zombies >= 10:
            print(f"Maximum zombie limit reached: {total_zombies} zombies")
            return

        # 기존 좀비들 미리 가져오기
        existing_zombies = game_world.get_objects_by_type(Zombie)

        # 이번에 소환할 좀비 수 계산
        zombies_to_spawn = min(self.spawn_count,
                              self.max_spawns_per_round - self.current_spawn_count)

        newly_spawned = []

        for i in range(zombies_to_spawn):
            # 스포너 주변 반경 내에서 랜덤 위치에 소환
            spawn_radius = 50 + i * 20  # 겹치지 않도록 반경 조정
            angle = random.uniform(0, 2 * math.pi)

            spawn_x = self.x + math.cos(angle) * spawn_radius
            spawn_y = self.y + math.sin(angle) * spawn_radius

            # 맵 경계 내로 제한
            spawn_x = max(50, min(2350, spawn_x))
            spawn_y = max(50, min(1750, spawn_y))

            # 좀비 생성
            zombie = Zombie(self.map, self.player, spawn_x, spawn_y)

            # 게임 월드에 추가
            game_world.add_object(zombie, 1)
            newly_spawned.append(zombie)

        # 새로 생성된 모든 좀비들의 기본 충돌 등록 (한 번에 처리)
        for zombie in newly_spawned:
            game_world.add_collision_pair("player:zombie", None, zombie)
            game_world.add_collision_pair("zombie:building", zombie, None)
            game_world.add_collision_pair("zombie:gun", zombie, None)

        # 좀비끼리의 충돌 등록 (중복 방지)
        for i, new_zombie in enumerate(newly_spawned):
            # 새 좀비와 기존 좀비들 간의 충돌
            for existing_zombie in existing_zombies:
                game_world.add_collision_pair("zombie:zombie", new_zombie, existing_zombie)

            # 새로 생성된 좀비들끼리의 충돌 (중복 방지: i < j만 등록)
            for j in range(i + 1, len(newly_spawned)):
                other_new_zombie = newly_spawned[j]
                game_world.add_collision_pair("zombie:zombie", new_zombie, other_new_zombie)

        self.current_spawn_count += zombies_to_spawn
        print(f"Round {self.round}: Spawned {zombies_to_spawn} zombies at ({self.x}, {self.y})")

    def draw(self):
        pass

    def clear(self):
        """리소스 정리"""
        pass

    def get_bb(self):
        """바운딩 박스 (필요시)"""
        # return (self.x - 10, self.y - 10, self.x + 10, self.y + 10)
        pass

    def handle_collision(self, key, other):
        """충돌 처리 (스포너는 충돌하지 않음)"""
        pass

    def set_active(self, active):
        """스포너 활성화/비활성화"""
        self.active = active

    def reset_for_new_round(self, new_round):
        """새 라운드를 위한 리셋"""
        self.round = new_round
        self.current_spawn_count = 0

        # 라운드에 따른 스포너 설정 업데이트
        self.spawn_interval = max(0.5, self.base_spawn_interval - (new_round - 1) * 0.3)
        self.spawn_count = self.base_spawn_count + (new_round - 1) // 2
        self.max_spawns_per_round = 5 + new_round * 3

        # 타이머 리셋
        self.spawn_timer = 0.0
        self.spawn_cooldown = self.spawn_interval

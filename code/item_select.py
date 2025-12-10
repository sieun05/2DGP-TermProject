from pico2d import *
from sdl2 import *
import game_framework
import common

class SelectItem:
    def __init__(self, x, y, kind='power'):
        self.x = x
        self.y = y
        self.kind = kind  # 'power', 'speed', 'maxhp' 등
        self.font = load_font('images/ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        # 선택 영역 가시화 (기본 동작 유지)
        draw_rectangle(*self.get_bb())
        # 종류 표시
        label = self.kind
        self.font.draw(self.x - 30, self.y - 80, label, (0, 0, 0))

    def clear(self):
        try:
            del self.font
        except Exception:
            pass

    def get_bb(self):
        return (self.x - 56, self.y - 64, self.x + 56, self.y + 64)

    def handle_collision(self, key, other):
        pass

    def clicked(self):
        # 이미 사용된 아이템이면 무시

        # 종류별 효과 적용
        if self.kind == 'power':
            # 공격력 증가
            if hasattr(common, 'player_attack_power') and common.gear >= 5:
                common.player_attack_power += 3
                common.gear -= 5
                print(f"player_attack_power -> {common.player_attack_power}")
        elif self.kind == 'speed':
            # 공격 속도 증가(초당 발사 수 증가)
            if hasattr(common, 'player_attack_speed') and common.gear >= 5:
                common.player_attack_speed += 1.0
                common.gear -= 5
                print(f"player_attack_speed -> {common.player_attack_speed}")
        elif self.kind == 'maxhp':
            # 최대 체력 증가
            if hasattr(common, 'player_max_heart') and common.apple >= 5:
                common.player_max_heart += 20
                common.apple -= 5
                common.player_heart = common.player_max_heart
                print(f"player_max_heart -> {common.player_max_heart}")
        else:
            print(f"Unknown item kind: {self.kind}")
        return True

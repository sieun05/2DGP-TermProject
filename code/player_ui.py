from pico2d import *
import common


class PlayerUI:
    def __init__(self):
        self.image = load_image('images/playmode_ui.png')
        self.player_health_image = load_image('images/heart_bar2.png')
        self.y=0

    def draw(self):
        # ...existing code...
        self.image.draw(400, 300)

        # heart_bar2.png 원본 크기
        max_w = 135
        h = 14

        # 안전한 비율 계산 (0..1)
        ratio = 0.0
        if getattr(common, 'player_max_heart', 0) > 0:
            ratio = max(0.0, min(1.0, common.player_heart / common.player_max_heart))

        cur_w = int(max_w * ratio)

        # 기존 코드가 중앙 x=726를 사용하므로, 왼쪽 기준 좌표 계산
        left_x = 726 - (max_w / 2)

        # pico2d의 clip_draw은 중심 좌표로 그리므로, 왼쪽 정렬을 위해서는
        # 중심 = 왼쪽 + 현재너비/2 를 사용
        if cur_w > 0:
            draw_x = left_x + (cur_w / 2)
            self.player_health_image.clip_draw(0, 0, cur_w, h, int(draw_x), 581)
        # ...existing code...

    def update(self):
        pass

    def clear(self):
        del self.image
        del self.player_health_image

    def get_bb(self):
        pass

    def handle_collision(self, key, other):
        pass


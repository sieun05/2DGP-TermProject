from pico2d import *
from sdl2 import *

class Building:
    def __init__(self, map, x, y, num):
        if num == 0:
            self.image = load_image('images/building.png')
        elif num == 1:
            self.image = load_image('images/building2.png')
        self.font = load_font('images/ENCR10B.TTF', 16)
        self.x = x
        self.y = y
        self.map=map

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 160, 250, self.x-(self.map.x), self.y-(self.map.y)+125)
        # self.font.draw(100, 400, f'({self.x}, {self.y})', (0, 0, 0))
        draw_rectangle(*self.get_bb())

    def clear(self):
        del self.image

    def get_bb(self):
        return (self.x-(self.map.x) - 80, self.y-(self.map.y),
                self.x-(self.map.x) + 80, self.y-(self.map.y) + 100)

    # self.x-(self.map.x), self.y-(self.map.y)+125

    def handle_collision(self, key, other):
        # if key == "player:building":
        #     print(f"Player collided with Building at ({other.x}, {other.y})")
        # elif key == "player:zombie":
        #     print(f"Player collided with Zombie at ({other.x}, {other.y})")
        pass

from pico2d import *
from sdl2 import *
import game_framework

class Car:
    sound = None

    def __init__(self):
        self.x = 520
        self.y = 480
        if Car.sound is None:
            Car.sound = load_wav('sounds/car_horn.wav')
            Car.sound.set_volume(64)

        self.To_play = False
        self.clicked_flag = False
        self.timer = 0.0

    def update(self):
        if  self.clicked_flag == True and get_time() - self.timer > 3.0:
            self.To_play = True
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def clear(self):
        pass

    def get_bb(self):
        return (self.x - 55, self.y - 60, self.x + 55, self.y + 60)

    def handle_collision(self, key, other):
        pass

    def clicked(self):
        if self.To_play == False:
            Car.sound.play()
            self.clicked_flag = True
            self.timer = get_time()
        pass

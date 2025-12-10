from pico2d import *
from sdl2 import *

class BGM_Title:
    def __init__(self):
        self.bgm = load_music('sounds/title.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

        self.y = 0
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def clear(self):
        del self.bgm


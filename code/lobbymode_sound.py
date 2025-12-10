from pico2d import *
from sdl2 import *

class BGM_Lobby:
    def __init__(self):
        self.bgm = load_music('sounds/lobby.mp3')
        self.bgm.set_volume(32)
        self.bgm.play()

        self.y = 0
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def clear(self):
        del self.bgm


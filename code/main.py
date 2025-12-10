from pico2d import *
import game_framework
import logo_mode, gameover_mode

open_canvas()
game_framework.run(gameover_mode)
close_canvas()
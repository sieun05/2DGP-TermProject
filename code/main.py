from pico2d import *
import sys
import os
import game_framework
from mode import logo_mode, play_mode, title_mode, lobby_mode, gameover_mode


open_canvas()
game_framework.run(lobby_mode)
close_canvas()
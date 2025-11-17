from pico2d import *
import sys
import os
import game_framework
from mode import logo_mode, play_mode


open_canvas()
game_framework.run(logo_mode)
close_canvas()
import ctypes
import os
import pygame as pg
from pygame import gfxdraw
from pygame.locals import *


def main():
    # anti - stretch for pygame
    ctypes.windll.user32.SetProcessDPIAware()
    pg.init()
    pg.font.init()
    pg.mouse.set_visible(True)

    sans = pg.font.Font(os.path.join('fonts', 'FantasqueSansMono-Regular.ttf'), 35)


if __name__ == '__main__':
    main()

import ctypes
import os
import pygame as pg
import pygame.image
from pygame import gfxdraw
from pygame.locals import *


def main():
    # anti - stretch for pygame
    ctypes.windll.user32.SetProcessDPIAware()
    pg.init()
    pg.font.init()
    pg.mouse.set_visible(True)

    sans = pg.font.Font(os.path.join('fonts', 'FantasqueSansMono-Regular.ttf'), 35)
    font = sans

    initial_size = [1920, 900]

    flags = pg.RESIZABLE

    screen = pg.display.set_mode(initial_size, flags)
    icon = pygame.image.load(os.path.join('graphics', 'icon.png'))
    pg.display.set_icon(icon)

    pg.display.set_caption("unNote")

    clock = pg.time.Clock()
    continue_running = True

    while continue_running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                continue_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                continue_running = False

    pg.quit()


def get_screen_size():
    screen_info = pg.display.Info()
    x = screen_info.current_w
    y = screen_info.current_h
    screen_size = [x, y]
    return screen_size


if __name__ == '__main__':
    main()

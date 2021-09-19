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
    font = sans

    initial_size = [1920, 900]

    flags = pg.RESIZABLE

    screen = pg.display.set_mode(initial_size, flags)

    pg.display.set_caption("unNote")

    clock = pg.time.Clock()
    continue_running = True

    while continue_running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                continue_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                continue_running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    key = "left"
                elif event.button == 5:
                    key = "right"

                pg.time.wait(200)

    pg.quit()


if __name__ == '__main__':
    main()

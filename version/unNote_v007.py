import ctypes
import os
import json
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

    background_color = pg.Color("white")

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

        window_info = divide_screen()
        clock.tick(60)

        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(background_color)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                continue_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                continue_running = False

        screen.blit(background, (0, 0))

        pg.display.update()

    pg.quit()


def get_screen_size():
    screen_info = pg.display.Info()
    x = screen_info.current_w
    y = screen_info.current_h
    screen_size = [x, y]
    return screen_size


def divide_screen():
    screen_size = get_screen_size()
    screen_ratio_x = 0.8
    screen_ratio_y = (screen_size[1] - 40) / screen_size[1]

    main_window_x = int(screen_size[0] * screen_ratio_x)
    main_window_y = int(screen_size[1] * screen_ratio_y)
    main_window = [0, 0, main_window_x, main_window_y]
    left_window = [main_window_x, 0, screen_size[0] - main_window_x, main_window_y]
    top_window = [0, 0, screen_size[0], screen_size[1] - main_window_y]
    window_info = [Rect(main_window), Rect(left_window), Rect(top_window)]
    # print(window_info)
    return window_info


def initialize_colors():
    with open(os.path.join('settings', 'colors.json')) as f:
        data = json.load(f)
        color = []
        for value in data:
            r = data[value][0]
            g = data[value][1]
            b = data[value][2]
            value = pg.Color(r, g, b)
            color.append(value)
        print(color)
        return color


def draw_corners(surface):
    color = pg.Color("orange")
    x = surface.get_width() - 1
    y = surface.get_height() - 1
    gfxdraw.pixel(surface, 0, 0, color)
    gfxdraw.pixel(surface, x, 0, color)
    gfxdraw.pixel(surface, 0, y, color)
    gfxdraw.pixel(surface, x, y, color)


if __name__ == '__main__':
    main()

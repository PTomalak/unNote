import os
# import json
import pygame as pg
import pygame.image
from pygame import gfxdraw
from pygame.locals import *
from os import environ
from sys import platform as _sys_platform


def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif _sys_platform in ('linux', 'linux2', 'linux3'):
        return "linux"
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'


def main():
    if platform() == "win":
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()

    pg.init()
    pg.font.init()
    pg.mouse.set_visible(True)

    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, K_ESCAPE, VIDEORESIZE, MOUSEBUTTONDOWN, MOUSEBUTTONDOWN, K_s])

    path = os.path.dirname(os.path.abspath(__file__)) + "/"

    background_color = pg.Color("black")
    morpheon = pg.Color(38, 50, 56)

    sans = pg.font.Font(str(path + "FantasqueSansMono-Regular.ttf"), 35)
    font = sans

    initial_size = [1920, 900]
    mouse_state = 0
    previous_mouse_state = 0
    line = []
    rubber = []
    tool = 0
    line_array = []
    page = [[]]
    current_page = 0
    max_page = 0
    min_page = 0

    flags = pg.RESIZABLE
    screen = pg.display.set_mode(initial_size, flags)

    pg.display.set_caption("unNote")

    clock = pg.time.Clock()
    continue_running = True

    while continue_running:

        window_info = divide_screen()
        if platform() == "win" or platform() == "linux":
            clock.tick(240)
        else:
            clock.tick(40)

        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(background_color)

        main_window = pg.Surface(window_info[0].size)
        main_window.fill(pg.Color("black"))
        left_window = pg.Surface(window_info[1].size)
        left_window.fill(pg.Color(morpheon))
        top_window = pg.Surface(window_info[2].size)
        top_window.fill(pg.Color("grey"))

        main_window = main_window.convert()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                continue_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                continue_running = False
            elif event.type == pg.VIDEORESIZE:
                initial_size[0], initial_size[1] = event.w, event.h
                screen = pg.display.set_mode(initial_size, flags)

            elif event.type == pg.KEYDOWN and event.key == K_s:
                if tool == 1:
                    tool = 0
                elif tool == 0:
                    tool = 1

            # states: 0-up 1-click_down 2-down 3-click_up 0-up 5-dot
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_state = 1
                if pg.Rect.collidepoint(left_window.get_bounding_rect(),
                                        get_cursor_pos()) and max_page == current_page and len(line_array) != 0:
                    max_page += 1
                    page[current_page] = line_array[:]
                    page.append([])
                    line_array.clear()
                    current_page += 1
                elif pg.Rect.collidepoint(top_window.get_bounding_rect(),
                                          get_cursor_pos()) and min_page != current_page:
                    page[current_page] = line_array[:]
                    line_array.clear()
                    current_page -= 1
                    line_array = page[current_page]
                elif pg.Rect.collidepoint(left_window.get_bounding_rect(),
                                          get_cursor_pos()) and max_page != current_page:
                    page[current_page] = line_array[:]
                    line_array.clear()
                    current_page += 1
                    line_array = page[current_page]
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_state = 0

        if window_info[0][0] > get_cursor_pos()[0] or window_info[0][1] > get_cursor_pos()[1]:
            mouse_state = 0
        elif get_cursor_pos()[0] >= get_screen_size()[0] - 1 or get_cursor_pos()[1] >= get_screen_size()[1] - 1:
            mouse_state = 0

        if mouse_state != previous_mouse_state:
            mouse_flip = 1
            previous_mouse_state = mouse_state
        else:
            mouse_flip = 0

        line_grapher(line, line_array, main_window)

        cursor_pos = get_cursor_pos()
        if tool == 0:
            current_line(line, line_array, mouse_flip, mouse_state)
        elif tool == 1:
            current_rubber(rubber, mouse_flip, mouse_state, line_array)
            rubber_grapher(rubber, main_window)

        text = pg.font.Font.render(font, "Page: " + str(current_page + 1) + "/" + str(max_page + 1), True, morpheon)

        screen.blit(background, (0, 0))

        screen.blit(main_window, window_info[0].topleft)
        screen.blit(left_window, window_info[1].topleft)
        screen.blit(top_window, window_info[2].topleft)

        screen.blit(text, window_info[2].topleft)

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
    main_window = [screen_size[0] - main_window_x, screen_size[1] - main_window_y, main_window_x, main_window_y]
    left_window = [0, screen_size[1] - main_window_y, screen_size[0] - main_window_x, main_window_y]
    top_window = [0, 0, screen_size[0], screen_size[1] - main_window_y]
    window_info = [Rect(main_window), Rect(left_window), Rect(top_window)]
    # print(window_info)
    return window_info


def get_cursor_pos():
    xPos, yPos = pygame.mouse.get_pos()
    return xPos, yPos


def current_line(line, line_array, mouse_flip, mouse_state):
    x, y = get_cursor_pos()
    window_info = divide_screen()
    if mouse_state == 1 and mouse_flip == 1 and window_info[0][0] <= x and window_info[0][1] <= y:
        line.append([x - window_info[0][0], y - window_info[0][1]])
    elif mouse_state == 1 and window_info[0][0] <= x and window_info[0][1] <= y:
        if line[-1] != [x - window_info[0][0], y - window_info[0][1]]:
            line.append([x - window_info[0][0], y - window_info[0][1]])
    elif mouse_state == 0 and mouse_flip == 1:
        if line[-1] != [x, y] and window_info[0][0] <= x and window_info[0][1] <= y:
            line.append([x - window_info[0][0], y - window_info[0][1]])
        line_array.append(line[:])
        line.clear()


def current_rubber(rubber, mouse_flip, mouse_state, line_array):
    x, y = get_cursor_pos()
    window_info = divide_screen()
    if mouse_state == 1 and mouse_flip == 1 and window_info[0][0] <= x and window_info[0][1] <= y:
        rubber.append([x - window_info[0][0], y - window_info[0][1]])
    elif mouse_state == 1 and window_info[0][0] <= x and window_info[0][1] <= y:
        if rubber[-1] != [x - window_info[0][0], y - window_info[0][1]]:
            rubber.append([x - window_info[0][0], y - window_info[0][1]])
    elif mouse_state == 0 and mouse_flip == 1:
        if rubber[-1] != [x, y] and window_info[0][0] <= x and window_info[0][1] <= y:
            rubber.append([x - window_info[0][0], y - window_info[0][1]])
        delete_line(line_array, rubber)
        rubber.clear()


def line_grapher(line, line_array, surface):
    color = pg.Color("white")
    # update = surface.get_bounding_rect()
    for i in line_array:
        pg.draw.lines(surface, color, False, i, width=2)
    if len(line) > 1:
        pg.draw.lines(surface, color, False, line)


def rubber_grapher(rubber, surface):
    color = pg.Color("red")
    # update = surface.get_bounding_rect()
    if len(rubber) > 1:
        pg.draw.lines(surface, color, False, rubber)


# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def side(a, b, c):
    """ Returns a position of the point c relative to the line going through a and b
        Points a, b are expected to be different
    """
    d = (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])
    return 1 if d > 0 else (-1 if d < 0 else 0)


def is_point_in_closed_segment(a, b, c):
    """ Returns True if c is inside closed segment, False otherwise.
        a, b, c are expected to be collinear
    """
    if a[0] < b[0]:
        return a[0] <= c[0] <= b[0]
    if b[0] < a[0]:
        return b[0] <= c[0] <= a[0]

    if a[1] < b[1]:
        return a[1] <= c[1] <= b[1]
    if b[1] < a[1]:
        return b[1] <= c[1] <= a[1]

    return a[0] == c[0] and a[1] == c[1]


#
def closed_segment_intersect(a, b, c, d):
    """ Verifies if closed segments a, b, c, d do intersect.
    """
    if a == b:
        return a == c or a == d
    if c == d:
        return c == a or c == b

    s1 = side(a, b, c)
    s2 = side(a, b, d)

    # All points are collinear
    if s1 == 0 and s2 == 0:
        return \
            is_point_in_closed_segment(a, b, c) or is_point_in_closed_segment(a, b, d) or \
            is_point_in_closed_segment(c, d, a) or is_point_in_closed_segment(c, d, b)

    # No touching and on the same side
    if s1 and s1 == s2:
        return False

    s1 = side(c, d, a)
    s2 = side(c, d, b)

    # No touching and on the same side
    if s1 and s1 == s2:
        return False

    return True


def delete_line(line_array, rubber):
    delete = -1
    if len(line_array) >= 1:
        for i in range(len(rubber)-1):
            for k in range(len(line_array)):
                for z in range(len(line_array[k])-1):
                    p1 = rubber[i]
                    p2 = rubber[i+1]
                    p3 = line_array[k][z]
                    p4 = line_array[k][z+1]
                    if closed_segment_intersect(p1, p2, p3, p4):
                        print(line_array[k])
                        delete = k

    if delete != -1:
        line_array.pop(delete)


if __name__ == '__main__':
    main()

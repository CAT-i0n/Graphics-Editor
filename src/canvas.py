import tkinter as tk
from time import sleep
from .shapes import DDA, BresenhamLine, WuLine


class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Button-1>', self.__position)
        self.bind('<Motion>', self.__motion)
        self._positions = []
        self._shapes = []

        self._mods = {'DDA': DDA,
                     'Bresenham': BresenhamLine,
                     'Wu': WuLine}

        self._isDraw: bool = False
        self.draw_mode = 'DDA'
        self.debug_mode = False

    def __position(self, event):
        if self._isDraw:
            x, y = event.x, event.y
            if len(self._positions) > 1:
                self._shapes.append(self.__draw_line(*self._positions[-1], x, y))
            self._isDraw = False
        else:
            x, y = event.x, event.y
            self._positions.append((x, y))
            self._shapes.append(self.__draw_line(x, y, x, y))
            self._isDraw = True

    def __motion(self, event):
        if self.debug_mode:
            return
        if self._isDraw:
            if len(self._shapes) > 1:
                self.__delete_last_line()
                pass
            if len(self._positions) > 0:
                # self.canvas.create_line(*self._positions[-1], event.x, event.y)
                self._shapes.append(self.__draw_line(
                    *self._positions[-1], event.x, event.y))

    def __draw_line(self, *args):
        points = []
        for i in self._mods[self.draw_mode]().draw(*args):
            if self.debug_mode:
                sleep(0.005)
                self.update()
            points.append(self.__draw_point(*i))
        return points

    def __draw_point(self, x, y, alpha=1):
        color = hex(int(255*(alpha)))[2:]*3
        return self.create_line(x, y, x+1, y, fill=f'#{color}')

    def __delete_last_line(self):
        if len(self._shapes) > 0:
            for i in self._shapes[-1]:
                self.delete(i)
            self._shapes = self._shapes[:-1]

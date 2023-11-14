import tkinter as tk
from time import sleep
from .point import Point
from .shapes import (DDA, BresenhamLine, WuLine,
                     Circle, Ellipse, Hyperbola, Parabola,
                     Hermite, Bеzier, Splain, ClosedSplain, Interpolation)

from .modes import CanvasModes
from .binds import TwoAnchorBinds, InterpolationBinds, EditBinds


class Canvas(tk.Canvas):
    id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = []
        self.positions = []
        self.shapes = []
        self.shape_draw_mode = 'DDA'

        self.isDraw: bool = False
        self.draw_mode = None
        self.mode = CanvasModes.DRAW
        self.button_clicked = -1
        self.approve = False
        self.move = 0

        self._shape_mods = {'DDA': DDA,
                            'Bresenham': BresenhamLine,
                            'Wu': WuLine,
                            'Circle': Circle,
                            'Ellipse': Ellipse,
                            'Hyperbola': Hyperbola,
                            'Parabola': Parabola,
                            'Hermite': Hermite,
                            'Bеzier': Bеzier,
                            'Splain': Splain,
                            'Closed splain': ClosedSplain}
        
        self._binds = None 
        self.change_draw_mode()

    def change_draw_mode(self):
        if self.mode == CanvasModes.EDIT:
            return
        self.unbind('<Button-1>')
        self.unbind('<Motion>')
        self.unbind('<Button-2>')
        if issubclass(self._shape_mods[self.shape_draw_mode], Interpolation):
            self._binds = InterpolationBinds(self)
        else:
            self._binds = TwoAnchorBinds(self)

        self.bind('<Button-1>', self._binds.position)
        self.bind('<Motion>', self._binds.motion)
        self.bind('<Button-3>', self._binds.approve)

        self.positions = []
        for i in self.buttons:
            self.delete(i)
        self.buttons = []

    def change_mode(self):
        if self.mode == CanvasModes.EDIT:
            self.unbind('<Button-1>')
            self.unbind('<Motion>')
            self.unbind('<Button-2>')

            self._binds = EditBinds(self)
            print(1)
            self.main_parent.bind('w', self._binds.up)
            print(1)


    def add_button(self, event):
        x, y = event.x, event.y
        self.positions.append((x, y))
        self.id += 1
        canvas_button = self.create_rectangle(
            x, y, x+15, y+15, fill="gray", tags="rect"+str(self.id))

        self.tag_bind("rect"+str(self.id), "<Button-1>",
                      lambda _: self.button_clicked(self.id))
        self.buttons.append(canvas_button)

    def button_clicked(self, num: int):
        self.button_clicked = num

    def draw_figure(self, *args):
        points = []
        shape = self._shape_mods[self.shape_draw_mode](*args)
        for i in shape.draw():
            if self.mode == CanvasModes.DEBUG:
                sleep(0.005)
                self.update()
            point = self.__draw_point(i)
            points.append(point)
        shape.points = points
        self.shapes.append(shape)

    def __draw_point(self, point):
        x, y, alpha = point.get_draw()
        self.id+=1
        color = hex(int(255*(alpha)))[2:]*3
        tag = "point" + str(self.id)
        index = self.create_line(x, y, x+1, y, fill=f'#{color}', tags=tag)
        point.set_id(index)
        point.set_tag(tag)
        return point

    def delete_last_line(self):
        if len(self.shapes) > 0:
            for i in self.shapes[-1].points:
                self.delete(i.get_id())
            self.shapes = self.shapes[:-1]

    def clear(self):
        for i in self.shapes:
            for j in i.points:
                self.delete(j.get_id())
        self.shapes = []
        self.isDraw: bool = False

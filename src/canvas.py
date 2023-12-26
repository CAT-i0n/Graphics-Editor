import tkinter as tk
from time import sleep
from .point import Point
from .shapes import (DDA, BresenhamLine, WuLine,
                     Circle, Ellipse, Hyperbola, Parabola,
                     Hermite, Bеzier, Splain, ClosedSplain, Interpolation,
                     DefaultPoly, Graham, Jarvis, Delone)

from .modes import CanvasModes
from .binds import TwoAnchorBinds, InterpolationBinds, EditBinds, PolyBinds, FillBinds


class Canvas(tk.Canvas):
    id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = []
        self.positions = []
        self.shapes = []
        self.shape_draw_mode = 'DDA'
        self.points = []
        self.isDraw: bool = False
        self.draw_mode = None
        self.mode = CanvasModes.DRAW
        self.button_clicked = -1
        self.approve = False

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
                            'Closed splain': ClosedSplain, 
                            'Default' : DefaultPoly, 
                            'Graham' : Graham,
                            'Jarvis': Jarvis,
                            'Delone' : Delone}
        
        self._binds = None 
        self.is_debug = None
        self.poly_mode = tk.StringVar()
        self.poly_check = tk.StringVar()
        self.color_var = tk.StringVar()
        # self.create_line(200,200,650,200, fill = "white")
        # self.create_line(200,500,650,500, fill = "white")
        # self.create_line(200,200,200,500, fill = "white")
        # self.create_line(650,200,650,500, fill = "white")
        
        self.change_draw_mode()        

    def change_draw_mode(self):
        self.unbind('<Button-1>')
        self.unbind('<Motion>')
        self.unbind('<Button-2>')
        if self.mode == CanvasModes.EDIT:
            self._binds = EditBinds(self)

            # self.main_parent.bind('r', self._binds.rot_xyz)
            self.main_parent.bind('r', lambda event: self._binds.transform(event, "rot_xyz"))

            self.main_parent.bind('w', lambda event: self._binds.transform(event, "rot_up"))
            self.main_parent.bind('s', lambda event: self._binds.transform(event, "rot_down"))
            self.main_parent.bind('d', lambda event: self._binds.transform(event, "rot_right"))
            self.main_parent.bind('a', lambda event: self._binds.transform(event, "rot_left"))
            self.main_parent.bind('q', lambda event: self._binds.transform(event, "rot_turn_left"))
            self.main_parent.bind('e', lambda event: self._binds.transform(event, "rot_turn_right"))

            self.main_parent.bind('=', lambda event: self._binds.transform(event, "scale_up"))
            self.main_parent.bind('-', lambda event: self._binds.transform(event, "scale_down"))

            self.main_parent.bind('<Left>', lambda event: self._binds.transform(event, "left"))
            self.main_parent.bind('<Right>', lambda event: self._binds.transform(event, "right"))
            self.main_parent.bind('<Up>', lambda event: self._binds.transform(event, "up"))
            self.main_parent.bind('<Down>', lambda event: self._binds.transform(event, "down"))

            self.main_parent.bind('p', lambda event: self._binds.transform(event, "perspective"))
            self.main_parent.bind('j', lambda event: self._binds.transform(event, "project"))
            return
        elif self.mode == CanvasModes.DRAW:
            if issubclass(self._shape_mods[self.shape_draw_mode], Interpolation):
                self._binds = InterpolationBinds(self)
            else:
                self._binds = TwoAnchorBinds(self)

            self.bind('<Button-1>', self._binds.position)
            self.bind('<Motion>', self._binds.motion)
            self.bind('<Button-3>', self._binds.approve)

            
        
        elif self.mode == CanvasModes.POLY:
            self._binds = PolyBinds(self)

            self.bind('<Button-1>', self._binds.position)
            self.bind('<Motion>', self._binds.motion)
            self.bind('<Button-3>', self._binds.approve)

        elif self.mode == CanvasModes.FILL:
            self._binds = FillBinds(self)

            self.bind('<Button-1>', self._binds.position)
            self.bind('<Motion>', self._binds.motion)
            self.bind('<Button-3>', self._binds.approve)

        self.positions = []
        for i in self.buttons:
            self.delete(i)
        self.buttons = []
            
            
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
            if self.is_debug.get():
                sleep(0.005)
                self.update()
            point = self.__draw_point(i)
            points.append(point)
        shape.points = points
        self.shapes.append(shape)

    def draw_poly(self, *args):
        shape = self._shape_mods[self.poly_mode.get()](*args)
        #self.check_poly(*args)

        for i in shape.draw():
            if self.is_debug.get():
                sleep(0.005)
                self.update()
            
            print(i)
            line = DDA(*i[0], *i[1]).draw()
            for point in line:
                shape.canvas_points.append(self.__draw_point(point))
            
        self.shapes.append(shape)

        # if self.poly_mode.get() == 'Graham' and self.poly_mode.get() == 'Jarvis':
        #     self.poly_check.set('Полигон\nвыпуклый')

    def check_poly(self, *args):
        vecs = []
        vecs.append((args[0][0]-args[-1][0], args[0][1]-args[-1][1]))
        for i, p in enumerate(args[:-1]):
            vecs.append((args[i+1][0]-p[0], args[i+1][1]-p[1]))

        s = []
        for i, v in enumerate(vecs[:-1]):
            if v[0]*vecs[i+1][1] - v[1]*vecs[i+1][0]>0:
                s.append(1)
            if v[0]*vecs[i+1][1] - v[1]*vecs[i+1][0]<0:
                s.append(-1)
        if len(set(s))==1:
            self.poly_check.set('Полигон\nвыпуклый')
        else:
            self.poly_check.set('Полигон\nвогнутый')

    def draw_point(self, point):
        return self.__draw_point(point)

    def __draw_point(self, point):
        x, y, color = point.get_draw()
        self.id+=1
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
        for i in self.points:
            self.delete(i.get_id())
        self.shapes = []
        self.isDraw: bool = False
    
    def draw_lines(self, lines):
        if self.shape_draw_mode == 'DDA':
            for i in lines:
                self.draw_figure(*i)
            
    def draw_poly_fig(self, lines):
        for line in lines:
            self.draw_poly(line[:3], line[3:6], line[6:9], line[9:])
        #self.draw_lines(lines)
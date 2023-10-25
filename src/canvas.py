import tkinter as tk
from time import sleep
from .shapes import (DDA, BresenhamLine, WuLine,
                     Circle, Ellipse, Hyperbola, Parabola,
                     Hermite, Bеzier, Splain, Interpolation)


class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._motion = self.__two_anchor_motion
        self._position = self.__two_anchor_position
        self.bind('<Button-1>', self._position)
        self.bind('<Motion>', self._motion)
        
        self._buttons = []
        self._positions = []
        self._shapes = []

        self._shape_mods = {'DDA': DDA,
                            'Bresenham': BresenhamLine,
                            'Wu': WuLine,
                            'Circle': Circle,
                            'Ellipse': Ellipse,
                            'Hyperbola': Hyperbola,
                            'Parabola': Parabola,
                            'Hermite': Hermite, 
                            'Bеzier' : Bеzier, 
                            'Splain' : Splain}

        self._isDraw: bool = False
        self.shape_draw_mode = 'DDA'
        self.draw_mode = None
        self.debug_mode = False
        self._button_clicked = -1
        self.move = 0

    def change_draw_mode(self):
        self.unbind('<Button-1>')
        self.unbind('<Motion>')
        if issubclass(self._shape_mods[self.shape_draw_mode], Interpolation):
            self._position = self.__interpolation_position
            self._motion = self.__interpolation_motion
        else:
            self._motion = self.__two_anchor_motion
            self._position = self.__two_anchor_position

        self.bind('<Button-1>', self._position)
        self.bind('<Motion>', self._motion)

        self._positions = []
        for i in self._buttons:
            self.delete(i)
        self._buttons = []

    def __interpolation_position(self, event):
        if len(self._positions) == 4:
            if self._button_clicked!=-1:
                if self.move == 0:
                    self.move = 1
                else:
                    self.move = 0
                    self._button_clicked = -1
            points = []
            for i in self._buttons:
                rect = self.coords(i)
                x = (rect[0] + rect[2])//2
                y = (rect[1] + rect[3])//2
                points.append((x,y))
            print(points)
            self.__delete_last_line()
            self._shapes.append(self.__draw_figure(*points))
        else:
            x, y = event.x, event.y
            self._positions.append((x, y))
            num = len(self._buttons)
            # pixel = tk.PhotoImage(width=1, height=1)
            # canvas_button = tk.Button(
            #     master=self, width=1, height=1, image=pixel, text=str(num) ,command=lambda: self.__button_clicked(num), compound='c')
            # canvas_button.place(x=x, y=y)
            canvas_button = self.create_rectangle(x, y, x+10, y+10, fill="gray",tags="rect"+str(num))

            self.tag_bind("rect"+str(num),"<Button-1>", lambda _: self.__button_clicked(num))
            self._buttons.append(canvas_button)
            if len(self._positions) == 4:
                self.__interpolation_position(event)
    
    def __button_clicked(self, num: int):
        self._button_clicked = num

    def __interpolation_motion(self, event):
        x, y = event.x, event.y
        if self._button_clicked!=-1:
            self.moveto("rect"+ str(self._button_clicked), x, y)
            points = []
            for i in self._buttons:
                rect = self.coords(i)
                x = (rect[0] + rect[2])//2
                y = (rect[1] + rect[3])//2
                points.append((x,y))
            self.__delete_last_line()
            self._shapes.append(self.__draw_figure(*points))

    def __two_anchor_position(self, event):
        if len(self._positions) == 1:
            x, y = event.x, event.y
            if len(self._positions) > 1:
                self._shapes.append(self.__draw_figure(
                    *self._positions[-1], x, y))
            self._positions = []
        else:
            x, y = event.x, event.y
            self._positions.append((x, y))
            self._shapes.append(self.__draw_figure(x, y, x, y))

    def __two_anchor_motion(self, event):
        if self.debug_mode:
            return
        if len(self._positions) == 1:
            if len(self._shapes) > 1:
                self.__delete_last_line()
                pass
            if len(self._positions) > 0:
                # self.canvas.create_line(*self._positions[-1], event.x, event.y)
                self._shapes.append(self.__draw_figure(
                    *self._positions[-1], event.x, event.y))

    def __draw_figure(self, *args):
        points = []
        for i in self._shape_mods[self.shape_draw_mode]().draw(*args):
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

    def clear(self):
        for i in self._shapes:
            for j in i:
                self.delete(j)
        self._shapes = []
        self._isDraw: bool = False

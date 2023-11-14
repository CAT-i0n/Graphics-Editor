from abc import ABC, abstractmethod
from .modes import CanvasModes

class Binds:
    def __init__(self, canvas):
        pass

    #ЛКМ
    @abstractmethod
    def position(self, event):
        pass
    
    #Движение мышки
    @abstractmethod
    def motion(self, event):
        pass
    
    #ПКМ
    @abstractmethod
    def approve(self, event):
        pass

class TwoAnchorBinds(Binds):
    def __init__(self, canvas):
        self.canvas = canvas

    def position(self, event):
        if len(self.canvas.positions) == 1:
            x, y = event.x, event.y
            self.canvas.shapes.append(self.canvas.draw_figure(
                *self.canvas.positions[-1], x, y))
            if self.canvas.mode == CanvasModes.DEBUG:
                return
            self.canvas.positions = []
        else:
            x, y = event.x, event.y
            self.canvas.positions.append((x, y))
            self.canvas.shapes.append(self.canvas.draw_figure(x, y, x, y))

    def motion(self, event):
        if self.canvas.mode == CanvasModes.DEBUG:
            return
        if len(self.canvas.positions) == 1:
            self.canvas.delete_last_line()
            self.canvas.shapes.append(self.canvas.draw_figure(
                *self.canvas.positions[-1], event.x, event.y))


class InterpolationBinds(Binds):
    def __init__(self, canvas):
        self.canvas = canvas

    def position(self, event):
        # if self.canvas._button_clicked != -1:
        #     if self.canvas.move == 0:
        #         self.canvas.move = 1
        #     else:
        #         self.canvas.move = 0
        #         self.canvas._button_clicked = -1
        #     #self.canvas.__delete_last_line()
        #     return
        if ((len(self.canvas.positions) == 3 and
                not self.canvas.shape_draw_mode == "Splain")
                or (self.canvas.shape_draw_mode == "Splain"
                    and self.canvas.approve
                    and len(self.canvas.positions) >= 4)):
            self.canvas.add_button(event)
            points = []
            for i in self.canvas.buttons:
                rect = self.canvas.coords(i)
                x = (rect[0] + rect[2])//2
                y = (rect[1] + rect[3])//2
                points.append((x, y))
            self.canvas.shapes.append(self.canvas.draw_figure(*points))
            for i in self.canvas.buttons:
                self.canvas.delete(i)
            self.canvas.buttons = []
            self.canvas.positions = []
        else:
            if not self.canvas.approve:
                self.canvas.add_button(event)

    def motion(self, event):
        x, y = event.x, event.y
        if self.canvas.button_clicked != -1:
            self.canvas.moveto("rect" + str(self.canvas.button_clicked), x, y)
            points = []
            for i in self.canvas.buttons:
                rect = self.canvas.coords(i)
                x = (rect[0] + rect[2])//2
                y = (rect[1] + rect[3])//2
                points.append((x, y))
            self.canvas.delete_last_line()
            self.canvas.shapes.append(self.canvas.draw_figure(*points))

    def approve(self, event):
        self.canvas.approve = True
        self.position(event)
        self.canvas.approve = False


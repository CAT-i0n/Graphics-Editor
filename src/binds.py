from abc import ABC, abstractmethod
from .modes import CanvasModes
import numpy as np
from math import cos, sin, pi
from time import time
from .point import Point

class Binds:
    def __init__(self, canvas):
        pass

    # ЛКМ
    @abstractmethod
    def position(self, event):
        pass

    # Движение мышки
    @abstractmethod
    def motion(self, event):
        pass

    # ПКМ
    @abstractmethod
    def approve(self, event):
        pass


class TwoAnchorBinds(Binds):
    def __init__(self, canvas):
        self.canvas = canvas

    def position(self, event):
        if len(self.canvas.positions) == 1:
            x, y = event.x, event.y
            self.canvas.draw_figure(
                *self.canvas.positions[-1], x, y)
            if self.canvas.mode == CanvasModes.DEBUG:
                return
            self.canvas.positions = []
        else:
            x, y = event.x, event.y
            self.canvas.positions.append((x, y))
            self.canvas.draw_figure(x, y, x, y)

    def motion(self, event):
        if self.canvas.mode == CanvasModes.DEBUG:
            return
        if len(self.canvas.positions) == 1:
            self.canvas.delete_last_line()
            self.canvas.draw_figure(
                *self.canvas.positions[-1], event.x, event.y)


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
            self.canvas.draw_figure(*points)
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
            self.canvas.draw_figure(*points)

    def approve(self, event):
        self.canvas.approve = True
        self.position(event)
        self.canvas.approve = False


class EditBinds(Binds):
    def __init__(self, canvas):
        self.canvas = canvas
        f = 1/2/pi
        self.scale_up_matrix = np.array([[1.1, 0,  0,   0],
                                         [0, 1.1,  0,   0],
                                         [0,   0, 1.1,  0],
                                         [0,   0,   0,  1]])
        
        self.scale_down_matrix = np.array([[0.9, 0,   0, 0],
                                           [0, 0.9,   0, 0],
                                           [0,   0, 0.9, 0], 
                                           [0,   0,   0, 1]])
        
        self.up_matrix = np.array([[1, 0, 0,  0],
                                   [0, 1, 0, -5],
                                   [0, 0, 1,  0], 
                                   [0, 0, 0,  1]])
        
        self.down_matrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 5],
                                     [0, 0, 1, 0], 
                                     [0, 0, 0, 1]])

        self.left_matrix = np.array([[1, 0, 0, -5],
                                     [0, 1, 0,  0],
                                     [0, 0, 1,  0], 
                                     [0, 0, 0,  1]])

        self.right_matrix = np.array([[1, 0, 0, 5],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0], 
                                      [0, 0, 0, 1]])

        self.z_rot_matrix = np.array([[cos(f), -sin(f), 0, 0],
                                      [sin(f),  cos(f), 0, 0],
                                      [0,            0, 1, 0], 
                                      [0,            0, 0, 1]])
        
        self.y_rot_matrix = np.array([[ cos(f), 0, sin(f), 0],
                                      [      0, 1,      0, 0],
                                      [-sin(f), 0, cos(f), 0], 
                                      [      0, 0,      0, 1]])
        
        self.x_rot_matrix = np.array([[1,      0,       0, 0],
                                      [0, cos(f), -sin(f), 0],
                                      [0, sin(f),  cos(f), 0],
                                      [0,      0,       0, 1]])
        

        self.m_z_rot_matrix = np.array([[cos(-f), -sin(-f), 0, 0],
                                        [sin(-f),  cos(-f), 0, 0],
                                        [0,            0,   1, 0], 
                                        [0,            0,   0, 1]])
        
        self.m_y_rot_matrix = np.array([[ cos(-f), 0, sin(-f), 0],
                                        [      0,  1,       0, 0],
                                        [-sin(-f), 0, cos(-f), 0], 
                                        [      0,  0,       0, 1]])
        
        self.m_x_rot_matrix = np.array([[1,       0,        0, 0],
                                        [0, cos(-f), -sin(-f), 0],
                                        [0, sin(-f),  cos(-f), 0],
                                        [0,       0,        0, 1]])
        
        self.perspective_matrix = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 1, 0], 
                                            [0, 0, -0.001, 1]])
        
        self.project_matrix = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, 0], 
                                            [0, 0, 0, 1]])
        
        self.xyz_rot_matrix = self.x_rot_matrix@self.y_rot_matrix@self.z_rot_matrix
        


    def transform(self, event, transform):
        for shape in self.canvas.shapes:
            for point in shape.points:
                match transform:
                    case "rot_xyz":
                        point.vec = np.dot(self.xyz_rot_matrix, point.vec)
                    case "rot_up":
                        point.vec = np.dot(self.x_rot_matrix, point.vec)
                    case "rot_down":
                        point.vec = np.dot(self.m_x_rot_matrix, point.vec)
                    case "rot_right":
                        point.vec = np.dot(self.m_y_rot_matrix, point.vec)
                    case "rot_left":
                        point.vec = np.dot(self.y_rot_matrix, point.vec)
                    case "rot_turn_left":
                        point.vec = np.dot(self.m_z_rot_matrix, point.vec)
                    case "rot_turn_right":
                        point.vec = np.dot(self.z_rot_matrix, point.vec)
                    case "scale_up":
                        point.vec = np.dot(self.scale_up_matrix, point.vec)
                    case "scale_down":
                        point.vec = np.dot(self.scale_down_matrix, point.vec)
                    case "up":
                        point.vec = np.dot(self.up_matrix, point.vec)
                    case "down":
                        point.vec = np.dot(self.down_matrix, point.vec)
                    case "right":
                        point.vec = np.dot(self.right_matrix, point.vec)
                    case "left":
                        point.vec = np.dot(self.left_matrix, point.vec)
                    case "perspective":
                        point.vec = np.dot(self.perspective_matrix, point.vec)
                    case "project":
                        point.vec = np.dot(self.project_matrix, point.vec)
                
                if point.vec[3]!=1:
                    point.vec /= point.vec[3]
                x, y = point.vec[0]+425, point.vec[1]+350

                self.canvas.delete(point.get_id())
                x, y, color = point.get_draw()
                new_point = Point(x, y, 0, point.get_alpha())
                self.canvas.id+=1
                tag = "point" + str(self.canvas.id)
                index = self.canvas.create_line(x, y, x+1, y, fill=f'#{color}', tags=tag)
                new_point.set_id(index)
                new_point.set_tag(tag)
                self.canvas.points.append(new_point)
                point = new_point

                self.canvas.moveto(point.get_id(), x, y)

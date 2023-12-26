from abc import ABC, abstractmethod
from .modes import CanvasModes
import numpy as np
from math import cos, sin, pi
from time import time
from .point import Point
from .shapes import Poly, DDA

import pyscreenshot as ImageGrab

import sys
sys.setrecursionlimit(1000000)

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
            if self.canvas.is_debug.get():
                return
            self.canvas.positions = []
        else:
            x, y = event.x, event.y
            self.canvas.positions.append((x, y))
            self.canvas.draw_figure(x, y, x, y)

    def motion(self, event):
        if self.canvas.is_debug.get():
            return
        if len(self.canvas.positions) == 1:
            self.canvas.delete_last_line()
            self.canvas.draw_figure(
                *self.canvas.positions[-1], event.x, event.y)


class InterpolationBinds(Binds):
    def __init__(self, canvas):
        self.canvas = canvas

    def position(self, event):
        if ((len(self.canvas.positions) == 3 and
                not self.canvas.shape_draw_mode in ["Splain", "Closed splain"])
                or (self.canvas.shape_draw_mode in ["Splain", "Closed splain"]
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

        self.y_rot_matrix = np.array([[cos(f), 0, sin(f), 0],
                                      [0, 1,      0, 0],
                                      [-sin(f), 0, cos(f), 0],
                                      [0, 0,      0, 1]])

        self.x_rot_matrix = np.array([[1,      0,       0, 0],
                                      [0, cos(f), -sin(f), 0],
                                      [0, sin(f),  cos(f), 0],
                                      [0,      0,       0, 1]])

        self.m_z_rot_matrix = np.array([[cos(-f), -sin(-f), 0, 0],
                                        [sin(-f),  cos(-f), 0, 0],
                                        [0,            0,   1, 0],
                                        [0,            0,   0, 1]])

        self.m_y_rot_matrix = np.array([[cos(-f), 0, sin(-f), 0],
                                        [0,  1,       0, 0],
                                        [-sin(-f), 0, cos(-f), 0],
                                        [0,  0,       0, 1]])

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
        w1 = 0
        w2 = 0
        w3 = 0
        k = 0
        for shape in self.canvas.shapes:
            for point in shape.points:
                k+=1
                p = point.get_poly()
                w1+=p[0]
                w2+=p[1]
                w3+=p[2]
        w1/=k
        w2/=k
        w3/=k

        for shape in self.canvas.shapes:
            if issubclass(type(shape), Poly):
                for point in shape.canvas_points:
                    self.canvas.delete(point.get_id())
                shape.canvas_points = []
                for i, point in enumerate(shape.points):
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

                    if point.vec[3] != 1:
                        point.vec /= point.vec[3]
                    x, y, z = point.vec[0]+425, point.vec[1]+350, point.vec[2]
                    shape.points[i] = Point(x,y,z)

                p1 =  shape.points[0].get_poly()
                p2 =  shape.points[1].get_poly()
                p3 =  shape.points[2].get_poly()
                p4 =  shape.points[3].get_poly()

                v1 = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
                v2 = (p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2])

                A = v1[1]*v2[2] - v2[1]*v1[2]
                B = v1[2]*v2[0] - v2[2]*v1[0]
                C = v1[0]*v2[1] - v2[0]*v1[1]
                D = -1*(A*p1[0] + B*p1[1] + C*p1[2])

                W = (w1,w2,w3)

                m = 1 if A*W[0] + B*W[1] + C*W[2] + D<0 else -1

                A = A*m
                B = B*m
                C = C*m
                D = D*m

                P = [0,0,-1000]

                if A*P[0] + B*P[1] + C*P[2] + D*0 > 0:                    

                    for j, point in enumerate(shape.points[:-1]):
                        x1, y1, _ = point.get_draw()
                        x2, y2, _ = shape.points[j+1].get_draw()
                        line = DDA(x1, y1, x2, y2).draw()
                        for point in line:
                            shape.canvas_points.append(self.canvas.draw_point(point))
                    
                    x1, y1, _ = shape.points[-1].get_draw()
                    x2, y2, _ = shape.points[0].get_draw()
                    line = DDA(x1, y1, x2, y2).draw()
                    for point in line:
                        shape.canvas_points.append(self.canvas.draw_point(point))

            else:
                for i, point in enumerate(shape.points):
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

                    if point.vec[3] != 1:
                        point.vec /= point.vec[3]
                    x, y, z = point.vec[0]+425, point.vec[1]+350, point.vec[2]

                    self.canvas.delete(point.get_id())
                    self.canvas.points.append(point)
                    _, _, color = point.get_draw()
                    new_point = Point(x, y, z, point.get_alpha())
                    self.canvas.id += 1

                    tag = "point" + str(self.canvas.id)
                    index = self.canvas.create_line(
                        x, y, x+1, y, fill=f'#{color}', tags=tag)
                    new_point.set_id(index)
                    new_point.set_tag(tag)
                    self.canvas.points.append(new_point)
                    shape.points[i] = new_point

                    self.canvas.moveto(shape.points[i].get_id(), x, y)

            # self.canvas.create_rectangle(0, 0, 850, 200, fill='black')
            # self.canvas.create_rectangle(0, 0, 200, 700, fill='black')


class PolyBinds(Binds):
    def __init__(self, canvas):
        self.canvas = canvas

    def position(self, event):
        if ((self.canvas.approve and len(self.canvas.positions) >= 4)):
            self.canvas.add_button(event)
            points = []
            for i in self.canvas.buttons:
                rect = self.canvas.coords(i)
                x = (rect[0] + rect[2])//2
                y = (rect[1] + rect[3])//2
                points.append((x, y))
            self.canvas.draw_poly(*points)
            for i in self.canvas.buttons:
                self.canvas.delete(i)
            self.canvas.buttons = []
            self.canvas.positions = []
        else:
            if not self.canvas.approve:
                self.canvas.add_button(event)

    def motion(self, event):
        pass

    def approve(self, event):
        self.canvas.approve = True
        self.position(event)
        self.canvas.approve = False

class FillBinds(Binds):
    def __init__(self, canvas):
        self.canvas = canvas

    def position(self, event):
        rx, ry = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        # x, y = cnvs.winfo_pointerx(), cnvs.winfo_pointery()
        self.image = ImageGrab.grab((rx, ry, rx+850, ry+700)) 

        self.drawed = set()
        self.draw_neighbors(event.x,event.y)
    
    def draw_neighbors(self,x,y):
        if x>850 or y>700 or x<0 or y<0:
            return
        if self.image.getpixel((x, y+1)) == (0,0,0) and (x, y+1) not in self.drawed:
            self.drawed.add((x,y+1))
            self.draw_pixel(x, y+1)
            self.draw_neighbors(x, y+1)
        if self.image.getpixel((x+1, y)) == (0,0,0) and (x+1, y) not in self.drawed:
            self.drawed.add((x+1,y))
            self.draw_pixel(x+1, y)
            self.draw_neighbors(x+1, y)
        if self.image.getpixel((x, y-1)) == (0,0,0) and (x, y-1) not in self.drawed:
            self.drawed.add((x,y-1))
            self.draw_pixel(x, y-1)
            self.draw_neighbors(x, y-1)
        if self.image.getpixel((x-1, y)) == (0,0,0) and (x-1, y) not in self.drawed:
            self.drawed.add((x-1,y))
            self.draw_pixel(x-1, y)
            self.draw_neighbors(x-1, y)
        print(len(self.drawed))

    def draw_pixel(self, x, y):
        self.canvas.create_line(x, y, x+1, y, fill=self.canvas.color_var.get())

    def motion(self, event):
        pass


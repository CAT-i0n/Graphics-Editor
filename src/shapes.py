from abc import ABC, abstractmethod
from math import inf
import numpy as np
from itertools import cycle
from .point import Point
from math import atan
import math
import numpy
from scipy.spatial import Delaunay

INTERPOLATION_CURVES_POINT_NUM = 500
class Shape(ABC):

    @abstractmethod
    def draw(self, *args, **kwargs):
        pass


class Circle(Shape):
    def __init__(self, *args):
        self.points = args

    def draw(self):
        x, y, x1, y1 = self.points
        points = []
        r = ((x-x1)**2+(y-y1)**2)**0.5

        delta = 0
        plot_x = x
        plot_y = y
        x = 0
        y = r

        while y > 0:
            points.append(Point(plot_x + x, plot_y + y))
            points.append(Point(plot_x + x, plot_y - y))
            points.append(Point(plot_x - x, plot_y + y))
            points.append(Point(plot_x - x, plot_y - y))
            if delta > 0:
                dd = abs((x+1)**2+(y-1)**2 - r**2)
                dv = abs((x)**2+(y-1)**2 - r**2)
                if dd > dv:
                    y -= 1
                    delta += -2*y + 1
                else:
                    x += 1
                    y -= 1
                    delta += 2*(x-y+1)
                continue
            if delta < 0:
                dd = abs((x+1)**2+(y-1)**2 - r**2)
                dh = abs((x+1)**2+(y)**2 - r**2)
                if dd > dh:
                    x += 1
                    delta += 2*x + 1
                else:
                    x += 1
                    y -= 1
                    delta += 2*(x-y+1)
                continue
            if delta == 0:
                x += 1
                y -= 1
                delta += 2*(x-y+1)
        return points


class Ellipse(Shape):
    def __init__(self, *args):
        self.points = args

    def draw(self):
        x, y, x1, y1 = self.points
        points = []
        a = abs(x-x1)
        b = abs(y-y1)

        delta = a**2+b**2-2*a**2*b
        plot_x = x
        plot_y = y
        x = 0
        y = b

        while y > 0:
            points.append(Point(plot_x + x, plot_y + y))
            points.append(Point(plot_x + x, plot_y - y))
            points.append(Point(plot_x - x, plot_y + y))
            points.append(Point(plot_x - x, plot_y - y))
            r = b**2*a**2
            if delta > 0:
                dd = abs(b**2*(x+1)**2+a**2*(y-1)**2 - r)
                dv = abs(b**2*(x)**2+a**2*(y-1)**2 - r)
                if dd > dv:
                    y -= 1
                    delta += a**2*(1-2*y)
                else:
                    x += 1
                    y -= 1
                    delta += b**2*(1+2*x) + a**2*(1-2*y)
                continue
            if delta < 0:
                dd = abs(b**2*(x+1)**2+a**2*(y-1)**2 - r)
                dh = abs(b**2*(x+1)**2+a**2*(y)**2 - r)
                if dd > dh:
                    x += 1
                    delta += b**2*(1+2*x)
                else:
                    x += 1
                    y -= 1
                    delta += b**2*(1+2*x) + a**2*(1-2*y)
                continue
            if delta == 0:
                x += 1
                y -= 1
                delta += b**2*(1+2*x) + a**2*(1-2*y)
        return points


class Hyperbola(Shape):
    def __init__(self, *args):
        self.points = args

    def draw(self):
        x, y, x1, y1 = self.points
        points = []
        a = abs(x-x1)
        b = abs(y-y1)
        if a == 0 or b == 0:
            return []
        delta = b**2+2*a*b**2-a**2
        plot_x = x
        plot_y = y
        x = a
        y = 0

        size_x = 850
        size_y = 700
        r = b**2*a**2
        while (0 < plot_x + x < size_x or 0 < plot_x - x < size_x) and (0 < plot_y + y < size_y or 0 < plot_y - y < size_y):
            points.append(Point(plot_x + x, plot_y + y))
            points.append(Point(plot_x + x, plot_y - y))
            points.append(Point(plot_x - x, plot_y + y))
            points.append(Point(plot_x - x, plot_y - y))
            if delta > 0:
                d = b**2*(1+2*x)
                if d > 0:
                    y += 1
                    delta -= a**2*(1+2*y)
                else:
                    x += 1
                    y += 1
                    delta += b**2*(1+2*x) - a**2*(1+2*y)
                continue
            if delta < 0:
                d = -a**2*(1+2*y)
                if d > 0:
                    x += 1
                    delta += b**2*(1+2*x)
                else:
                    x += 1
                    y += 1
                    delta += b**2*(1+2*x) - a**2*(1+2*y)
                continue
            if delta == 0:
                x += 1
                y += 1
                delta += b**2*(1+2*x) - a**2*(1+2*y)
        return points


class Parabola(Shape):
    def __init__(self, *args):
        self.points = args

    def draw(self):
        x, y, x1, y1 = self.points
        points = []
        a = abs(x1-x)
        b = abs(y-y1)

        if a == 0 or b == 0:
            return []
        p = 2*a

        plot_x = x
        plot_y = y
        x = 0
        y = 0

        delta = - 2 * p + 1

        size_x = 850
        size_y = 700
        r = 2*p
        while (0 < plot_x + x < size_x or 0 < plot_x - x < size_x) and (0 < plot_y + y < size_y or 0 < plot_y - y < size_y):
            points.append(Point(plot_x + x, plot_y + y))
            points.append(Point(plot_x + x, plot_y - y))
            if delta < 0:
                d = 2*p
                if d > 0:
                    y += 1
                    delta += 2*y+1
                else:
                    x += 1
                    y += 1
                    delta += 2*y+1 - 2*p
                continue
            if delta > 0:
                d = 2*y+1
                if d > 0:
                    x += 1
                    delta -= 2*p
                else:
                    x += 1
                    y += 1
                    delta += 2*y+1 - 2*p
                continue
            if delta == 0:
                x += 1
                y += 1
                delta += 2*y+1 - 2*p
        return points


class DDA():
    def __init__(self, *args):
        self.points = args
        

    def draw(self):
        if len(self.points) == 4:
            x1, y1, x2, y2 = self.points
            if x1-x2 == 0 and y1-y2 == 0:
                return [Point(x1, y1)]
            points = []

            length = max(abs(x1-x2), abs(y1-y2))
            dx = (x2-x1)/length
            dy = (y2-y1)/length
            x = x1
            y = y1
            i = 0
            while i < length+1:
                x += dx
                y += dy
                points.append(Point(x, y))
                i += 1
            return points
        elif len(self.points) == 6:
            x1, y1, z1, x2, y2, z2 = self.points
            x1 += 425
            x2 += 425
            y1 += 350
            y2 += 350
            points = []

            length = max(abs(x1-x2), abs(y1-y2), abs(z1-z2))
            dx = (x2-x1)/length
            dy = (y2-y1)/length
            dz = (z2-z1)/length
            x = x1
            y = y1
            z = z1
            i = 0
            while i < length:
                x += dx
                y += dy
                z += dz
                points.append(Point(x, y, z))
                i += 1
            return points

class BresenhamLine():
    def __init__(self, *args):
        self.points = args

    def draw(self):
        x1, y1, x2, y2 = self.points
        if x1-x2 == 0 and y1-y2 == 0:
            return [Point(x1, y1)]
        points = []

        steep = abs(y2 - y1) > abs(x2 - x1)

        if abs(y2 - y1) > abs(x2 - x1):
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        ystep = 1 if y1 < y2 else -1

        x, y = x1, y1
        dx = x2 - x1
        dy = abs(y2 - y1)
        e = 2*dy-dx
        i = 1
        while i < dx:
            if e > 0:
                y += ystep
                e -= 2*dx
            x += 1
            e += 2*dy
            i += 1
            if steep:
                points.append(Point(y, x))
            else:
                points.append(Point(x, y))

        return points


class WuLine():
    def __init__(self, *args):
        self.points = args

    def draw(self):
        x1, y1, x2, y2 = self.points
        if x1-x2 == 0 and y1-y2 == 0:
            return [Point(x1, y1)]

        steep = abs(y2 - y1) > abs(x2 - x1)

        if abs(y2 - y1) > abs(x2 - x1):
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        points = []

        if steep:
            points.append(Point(y1, x1, 0, 1))
        else:
            points.append(Point(x2, y2, 0, 1))
        dx = x2 - x1
        dy = y2 - y1
        gradient = dy / dx
        y = y1 + gradient
        for x in range(x1+1, x2):
            if steep:
                points.append(Point(int(y), x, 0, 1 - (y - int(y))))
                points.append(Point(int(y) + 1, x, 0, y - int(y)))
            else:
                points.append(Point(x, int(y), 0, 1 - (y - int(y))))
                points.append(Point(x, int(y) + 1, 0, y - (int(y))))

            y += gradient
        return points


class Interpolation:
    ...


class Hermite(Shape, Interpolation):
    def __init__(self, *args):
        self.points = args

    def draw(self):

        max_x = max(list(zip(*self.points))[0])
        max_y = max(list(zip(*self.points))[1])

        max_p = max(max_x, max_y)

        normalized = []

        for i, j in enumerate(self.points):
            normalized.append((j[0]/max_p, j[1]/max_p))

        p1, p2, p3, p4 = normalized

        tx = [2*p1[0]-2*p2[0]+p3[0]+p4[0],
              -3*p1[0]+3*p2[0]-2*p3[0]-p4[0],
              p3[0],
              p1[0]]

        ty = [2*p1[1]-2*p2[1]+p3[1]+p4[1],
              -3*p1[1]+3*p2[1]-2*p3[1]-p4[1],
              p3[1],
              p1[1]]

        points = []

        for i in np.arange(0, 1, 1/INTERPOLATION_CURVES_POINT_NUM):
            x = 0
            y = 0
            for j in range(4):
                p = -1*j+3
                x += i**p*tx[j]*max_p
                y += i**p*ty[j]*max_p
            points.append(Point(x, y))

        return points


class Bеzier(Shape, Interpolation):
    def __init__(self, *args):
        self.points = args

    def draw(self):

        max_x = max(list(zip(*self.points))[0])
        max_y = max(list(zip(*self.points))[1])

        max_p = max(max_x, max_y)

        normalized = []

        for i, j in enumerate(self.points):
            normalized.append((j[0]/max_p, j[1]/max_p))

        p1, p2, p3, p4 = normalized

        tx = [-1*p1[0]+3*p2[0]-3*p3[0]+p4[0],
              3*p1[0]-6*p2[0]+3*p3[0],
              -3*p1[0]+3*p2[0],
              p1[0]]

        ty = [-1*p1[1]+3*p2[1]-3*p3[1]+p4[1],
              3*p1[1]-6*p2[1]+3*p3[1],
              -3*p1[1]+3*p2[1],
              p1[1]]

        points = []

        for i in np.arange(0, 1, 1/INTERPOLATION_CURVES_POINT_NUM):
            x = 0
            y = 0
            for j in range(4):
                p = -1*j+3
                x += i**p*tx[j]*max_p
                y += i**p*ty[j]*max_p
            points.append(Point(x, y))

        return points


class ClosedSplain(Shape, Interpolation):
    def __init__(self, *args):
        self.points = args

    def draw(self, *args):

        max_x = max(list(zip(*self.points))[0])
        max_y = max(list(zip(*self.points))[1])

        max_p = max(max_x, max_y)

        normalized = []

        for i, j in enumerate(self.points):
            normalized.append((j[0]/max_p, j[1]/max_p))

        size = len(normalized)
        points = []
        for k in range(size):
            p1, p2, p3, p4 = normalized[k % size], normalized[(
                k+1) % size], normalized[(k+2) % size], normalized[(k+3) % size]

            tx = [-1*p1[0]+3*p2[0]-3*p3[0]+p4[0],
                  3*p1[0]-6*p2[0]+3*p3[0],
                  -3*p1[0]+3*p3[0],
                  p1[0]+4*p2[0]+p3[0]]

            ty = [-1*p1[1]+3*p2[1]-3*p3[1]+p4[1],
                  3*p1[1]-6*p2[1]+3*p3[1],
                  -3*p1[1]+3*p3[1],
                  p1[1]+4*p2[1]+p3[1]]

            for i in np.arange(0, 1, 1/INTERPOLATION_CURVES_POINT_NUM):
                x = 0
                y = 0
                for j in range(4):
                    p = -1*j+3
                    x += i**p*tx[j]*max_p/6
                    y += i**p*ty[j]*max_p/6
                points.append(Point(x, y))

        return points


class Splain(Shape, Interpolation):
    def __init__(self, *args):
        self.points = args

    def draw(self, *args):

        max_x = max(list(zip(*self.points))[0])
        max_y = max(list(zip(*self.points))[1])

        max_p = max(max_x, max_y)

        normalized = []

        for i, j in enumerate(self.points):
            normalized.append((j[0]/max_p, j[1]/max_p))

        size = len(normalized)
        points = []
        for k in range(size-1):
            p1, p2, p3, p4 = normalized[k % size], normalized[(
                k+1) % size], normalized[(k+2) % size], normalized[(k+3) % size]

            tx = [-1*p1[0]+3*p2[0]-3*p3[0]+p4[0],
                  3*p1[0]-6*p2[0]+3*p3[0],
                  -3*p1[0]+3*p3[0],
                  p1[0]+4*p2[0]+p3[0]]

            ty = [-1*p1[1]+3*p2[1]-3*p3[1]+p4[1],
                  3*p1[1]-6*p2[1]+3*p3[1],
                  -3*p1[1]+3*p3[1],
                  p1[1]+4*p2[1]+p3[1]]

            for i in np.arange(0, 1, 1/INTERPOLATION_CURVES_POINT_NUM):
                x = 0
                y = 0
                for j in range(4):
                    p = -1*j+3
                    x += i**p*tx[j]*max_p/6
                    y += i**p*ty[j]*max_p/6
                points.append(Point(x, y))

        return points

class Poly:
    ...

class DefaultPoly(Shape, Poly):
    def __init__(self, *args):
        self.points = args
        self.lines = []
        self.canvas_points = []

    def draw(self, *args):
        for i, point in enumerate(self.points[:-1]):
            self.lines += [(point, self.points[i+1])]

        self.lines += [(self.points[-1], self.points[0])]
        
        if len(self.points[0])==2:
            self.points = [Point(i[0], i[1]) for i in self.points]
        else:
            self.points = [Point(i[0]+425, i[1]+350, i[2]) for i in self.points]
        return self.lines
    



class Graham(Shape, Poly):
    def __init__(self, *args):
        self.points = args

    def draw(self, *args):
        points = []
        poly_points = []

        self.points = sorted(self.points, key = lambda x:[x[0],x[1]])
        start = self.points[0]
        poly_points.append(start)
        pol_angle = lambda y: (y[1]-start[1])/(y[0]-start[0]) if start[0]!=y[0] else 10000

        poss = sorted(self.points[1:], key = pol_angle)
        poly_points.append(poss[0])

        for i in poss[1:]:
            # u = (poly_points[-1][0] - i[0], poly_points[-1][1] - i[1])
            # v = (poly_points[-2][0] - i[0], poly_points[-2][1] - i[1])
            u = (poly_points[-1][0] - poly_points[-2][0], poly_points[-1][1] - poly_points[-2][1])
            v = (i[0] - poly_points[-1][0], i[1] - poly_points[-1][1])
            e = u[0]*v[1] - v[0]*u[1]
            if e>=0:
                poly_points.append(i)
            elif len(poly_points)>2:
                poly_points = poly_points[:-1]


        for i, point in enumerate(poly_points[:-1]):
            points += DDA(*point, *poly_points[i+1]).draw() 
        points += DDA(*poly_points[-1], *poly_points[0]).draw() 

        return points
        

class Jarvis(Shape, Poly):
    def __init__(self, *args):
        self.points = args

    def draw(self, *args):
        points = []

        def ConvexHull(pts):
            convex_hull=[] # Result array which gets appended over loops
            start_pt=pts[0] # This array will (ultimately) store the value of bottom-right-most point in X-Y plane. This is where we start gift wrapping from.
            start_id=0 # Just for swapping purpose
            for x in range(1,len(pts)): # Loop to find out the bottom-right-most point.
                if(pts[x][1]<start_pt[1]):
                    start_pt=pts[x]
                    start_id=x
                elif (pts[x][1]==start_pt[1] and pts[x][0]>start_pt[0]):
                    start_pt=pts[x]
                    start_id=x
            convex_hull.append(start_pt) # First element of convex hull
            pts[0],pts[start_id]=pts[start_id],pts[0] # Modifying the input array so that our first element goes to the 0th array position. Done by swapping.
            current_pt=start_pt # To store the last found point on convex hull. Necessary for calculating angles.
            last_angle=math.pi # To store angle made by last 2 points on convex hull. Used for checking a condition which says that no new point on the hull paired with the last found point can make an angle larger than the 2nd last found point paired with the last point.
            while(pts[0]==start_pt): # Main loop. Continues as long as a closed loop is not formed.
                max_angle=-(math.pi) # Starting from -180 degree. This comes from the fact that we started with the bottom-right-most point.
                for i in range(len(pts)):
                    angle=math.atan2((pts[i][1]-current_pt[1]),(pts[i][0]-current_pt[0]))
                    if(angle>=max_angle and angle<last_angle):
                        max_angle=angle
                        temp_pt=pts[i]
                if(temp_pt!=current_pt):
                    convex_hull.append(temp_pt)
                    current_pt=temp_pt
                    pts.remove(temp_pt)
                    last_angle=max_angle
                elif(temp_pt==start_pt):
                    break
            del convex_hull[-1] # To remove last element in result array which is the same as the first element.
            return convex_hull
        rez = ConvexHull(list(self.points))

        for i, point in enumerate(rez[:-1]):
            points += DDA(*point, *rez[i+1]).draw() 
        points += DDA(*rez[-1], *rez[0]).draw() 


        return points
        

class Delone(Shape, Poly):
    def __init__(self, *args):
        self.points = args

    def draw(self, *args):
        points = []
        tringles = Delaunay(self.points).simplices
        for i in tringles:
            points+=DDA(*self.points[i[0]], *self.points[i[1]]).draw() 
            points+=DDA(*self.points[i[1]], *self.points[i[2]]).draw() 
            points+=DDA(*self.points[i[2]], *self.points[i[0]]).draw()

        return points 

from abc import ABC, abstractmethod
from math import inf
import numpy as np 
from itertools import cycle
class Shape(ABC):
    points = []

    @abstractmethod
    def draw(self, *args, **kwargs):
        pass


class Circle(Shape):
    ...

    def draw(self, x, y, x1, y1):
        points = []
        r = ((x-x1)**2+(y-y1)**2)**0.5

        delta = 0
        plot_x = x
        plot_y = y
        x = 0
        y = r

        while y > 0:
            points.append((plot_x + x, plot_y + y))
            points.append((plot_x + x, plot_y - y))
            points.append((plot_x - x, plot_y + y))
            points.append((plot_x - x, plot_y - y))
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
    def draw(self, x, y, x1, y1):
        points = []
        a = abs(x-x1)
        b = abs(y-y1)

        delta = a**2+b**2-2*a**2*b
        plot_x = x
        plot_y = y
        x = 0
        y = b

        while y > 0:
            points.append((plot_x + x, plot_y + y))
            points.append((plot_x + x, plot_y - y))
            points.append((plot_x - x, plot_y + y))
            points.append((plot_x - x, plot_y - y))
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
    def draw(self, x, y, x1, y1):
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
            points.append((plot_x + x, plot_y + y))
            points.append((plot_x + x, plot_y - y))
            points.append((plot_x - x, plot_y + y))
            points.append((plot_x - x, plot_y - y))
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
    def draw(self, x, y, x1, y1):

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
            points.append((plot_x + x, plot_y + y))
            points.append((plot_x + x, plot_y - y))
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

    def draw(self, x1, y1, x2, y2):
        if x1-x2 == 0 and y1-y2 == 0:
            return [(x1, y1)]
        points = []

        length = max(abs(x1-x2), abs(y1-y2))
        dx = (x2-x1)/length
        dy = (y2-y1)/length
        x = x1
        y = y1
        i = 0
        while i < length:
            x += dx
            y += dy
            points.append((x, y))
            i += 1
        return points


class BresenhamLine():
    def draw(self, x1=0, y1=0, x2=0, y2=0):
        if x1-x2 == 0 and y1-y2 == 0:
            return [(x1, y1)]
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
                points.append((y, x))
            else:
                points.append((x, y))

        return points


class WuLine():

    def draw(self, x1, y1, x2, y2):
        if x1-x2 == 0 and y1-y2 == 0:
            return [(x1, y1)]

        steep = abs(y2 - y1) > abs(x2 - x1)

        if abs(y2 - y1) > abs(x2 - x1):
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        points = []

        if steep:
            points.append((y1, x1, 1))
        else:
            points.append((x2, y2, 1))
        dx = x2 - x1
        dy = y2 - y1
        gradient = dy / dx
        y = y1 + gradient
        for x in range(x1+1, x2):
            if steep:
                points.append((int(y), x, 1 - (y - int(y))))
                points.append((int(y) + 1, x, y - int(y)))
            else:
                points.append((x, int(y), 1 - (y - int(y))))
                points.append((x, int(y) + 1, y - (int(y))))

            y += gradient
        return points

class Interpolation:
    ...

class Hermite(Shape, Interpolation):
    def draw(self, *args):
        

        max_x = max(list(zip(*args))[0])
        max_y = max(list(zip(*args))[1])

        max_p = max(max_x, max_y)

        normalized = []

        for i,j in enumerate(args):
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

        for i in np.arange(0, 1, 0.001):
            x = 0
            y = 0
            for j in range(4):
                p = -1*j+3
                x+=i**p*tx[j]*max_p
                y+=i**p*ty[j]*max_p
            points.append((x,y))
            
        return points
    
class Bеzier(Shape, Interpolation):
    def draw(self, *args):
        

        max_x = max(list(zip(*args))[0])
        max_y = max(list(zip(*args))[1])

        max_p = max(max_x, max_y)

        normalized = []

        for i,j in enumerate(args):
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

        for i in np.arange(0, 1, 0.001):
            x = 0
            y = 0
            for j in range(4):
                p = -1*j+3
                x+=i**p*tx[j]*max_p
                y+=i**p*ty[j]*max_p
            points.append((x,y))
            
        return points
    
class Splain(Shape, Interpolation):
    def draw(self, *args):
        

        max_x = max(list(zip(*args))[0])
        max_y = max(list(zip(*args))[1])

        max_p = max(max_x, max_y)

        normalized = []

        for i,j in enumerate(args):
            normalized.append((j[0]/max_p, j[1]/max_p))

        size = len(normalized)
        points = []
        for k in range(size):
            p1, p2, p3, p4 = normalized[k%size], normalized[(k+1)%size], normalized[(k+2)%size], normalized[(k+3)%size]
            
            tx = [-1*p1[0]+3*p2[0]-3*p3[0]+p4[0],
                3*p1[0]-6*p2[0]+3*p3[0],
                -3*p1[0]+3*p3[0],
                p1[0]+4*p2[0]+p3[0]]
            
            ty = [-1*p1[1]+3*p2[1]-3*p3[1]+p4[1],
                3*p1[1]-6*p2[1]+3*p3[1],
                -3*p1[1]+3*p3[1],
                p1[1]+4*p2[1]+p3[1]]
        
            for i in np.arange(0, 1, 0.001):
                x = 0
                y = 0
                for j in range(4):
                    p = -1*j+3
                    x+=i**p*tx[j]*max_p/6
                    y+=i**p*ty[j]*max_p/6
                points.append((x,y))
                
        return points
    
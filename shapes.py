from abc import ABC, abstractmethod

class Shape(ABC):
    points = []

    @abstractmethod
    def draw(self, *args, **kwargs):
        pass

class Line(Shape):
    ...

    def draw(self, x1, y1, x2, y2):
        ...

class DDA(Line):
    
    def draw(self, x1, y1, x2, y2):
        if x1-x2 == 0 and y1-y2 == 0:
            return [(x1, y1)]
        points = []

        lenght = max(abs(x1-x2), abs(y1-y2))
        dx = (x2-x1)/lenght
        dy = (y2-y1)/lenght
        x = x1
        y = y1
        i = 0
        while i < lenght:
            x += dx
            y += dy
            points.append((x, y))
            i += 1
        return points
    

class BresenhamLine(Line):

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
    
class WuLine(Line):

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
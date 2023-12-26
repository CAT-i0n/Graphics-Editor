import numpy as np
class Point:
    def __init__(self, x, y, z = 0, alpha = 1):
        self._x = x
        self._y = y
        self._z = z
        self._alpha = alpha
        self._color = hex(int(255*(alpha)))[2:]*3
        self._tag = ""
        self._id = None
        self.vec = np.array([self._x-425, self._y-350, self._z, 1])
    
    def get_alpha(self):
        return self._alpha

    def get_draw(self):
        return self._x, self._y, self._color
    
    def get_poly(self):
        return (self._x-425, self._y-350, self._z)
    
    def get_id(self):
        return self._id
    
    def get_tag(self):
        return self._tag
    
    def set_id(self, id):
        self._id = id
    
    def set_tag(self, tag):
        self._tag = tag

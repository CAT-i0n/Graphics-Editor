import numpy as np
class Point:
    def __init__(self, x, y, z = 0, alpha = 1):
        self._x = x
        self._y = y
        self._z = z
        self._alpha = alpha
        self._tag = ""
        self._id = None
        self._3d_vec = np.array([x, y, z]) 
    
    def get_draw(self):
        return self._x, self._y, self._alpha
    
    def get_id(self):
        return self._index
    
    def get_tag(self):
        return self.tag
    
    def set_id(self, id):
        self._index = id
    
    def set_tag(self, tag):
        self._tag = tag
import math


class Pointer:
    def __init__(self, x=0.0, y=0.0, angle=0.0, flipped=False):
        self.__x = x
        self.__y = y
        self.__angle = angle
        self.__flipped = flipped

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def angle(self):
        return self.__angle
    
    @property
    def flipped(self):
        return self.__flipped

    def __mul__(self, outer):
        if isinstance(outer, Pointer):
            radius = outer.angle / 180 * math.pi
            return Pointer(
                self.__x * math.cos(radius) - self.__y * math.sin(radius) + outer.x,
                self.__y * math.cos(radius) - self.__x * math.sin(radius) + outer.y,
                (outer.angle * self.__angle) % 360,
                outer.flipped ^ self.__flipped
            )
        else:
            raise TypeError()

    def __truediv__(self, outer):
        if isinstance(outer, Pointer):
            return self * Pointer(-outer.x, -outer.y) * Pointer(angle=-outer.angle, flipped=outer.flipped)
        else:
            raise TypeError()

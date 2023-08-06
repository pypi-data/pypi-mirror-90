from .Generalfunction import Function
from turtle import Vec2D
import matplotlib.pyplot as plt


class Snowflake(Function):
    
    
    def __init__(self, theta=1):
        """
        init snowflake koch function
        """
        Function.__init__(self)
        self.theta = theta
        self.sqr_3 = 3.0 ** 0.5
        
    
    def kochSnowflakeImpl(self, p1, p2):
        u = p2 - p1
        v = Vec2D(-u[1], u[0])

        n1 = p1 + u * (1.0 / 3.0)
        n2 = n1 + u * (1.0 / 6.0) + v * (self.sqr_3 / 6.0)
        n3 = p1 + u * (2.0 / 3.0)

        return [p1, n1, n2, n3, p2]
    
    
    def kochSnowflake(self, level):
        p1 = Vec2D(0.0, 0.0)
        p2 = Vec2D(0.5, self.sqr_3 / 2.0)
        p3 = Vec2D(1.0, 0.0)

        array = [p1, p2, p3, p1]
   
        for _ in range(level):
            new_array = []

            for (p1, p2) in zip(array, array[1:]):
                new_array.extend(self.kochSnowflakeImpl(p1, p2))

            array = new_array

        return array
    
    
    def plot(self):
        points = self.kochSnowflake(self.theta)
        x, y = zip(*points)
        plt.plot(x, y)
        plt.show()
    
    
    def __repr__(self):
        """ 
        fuction to output the characteristics of the function
        """
        return "snowflake function with theta = {}".format(self.theta)

import math
class Point(object):
    """docstring for Point."""

    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return "( {} , {} )".format(self.x, self.y)

# 4,7,3,0
# 0,4,7,3


route = []
allfitness = []
route.append(Point(4.0, 0.0))
route.append(Point(7.0, 4.0))
route.append(Point(3.0, 7.0))
route.append(Point(0.0, 3.0))

def calcfitness():
    allfitness.clear()
    fitness = 0
    for point in range(len(route) - 1):
        dx2 = (route[point].x - route[point + 1].x)**2
        dy2 = (route[point].y - route[point + 1].y)**2
        dist = math.sqrt(dx2 + dy2)
        fitness += dist
        print("I AM POINT ", route[point], "LOOKING TO ", route[point+1])
        print("DELTA X: ", dx2)
        print("DELTA Y: ", dy2)
        print()
    dx2 = (route[-1].x - route[0].x)**2
    dy2 = (route[-1].y - route[0].y)**2
    dist = math.sqrt(dx2 + dy2)
    fitness += dist
    print("I AM POINT ", route[-1], "LOOKING TO ", route[0])
    print()
    allfitness.append(fitness)

calcfitness()
print(allfitness)

import random
import math

class Point(object):
    """docstring for Point."""

    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return "( {} , {} )".format(self.x, self.y)


class PointSet(object):
    """Descripbes one input"""

    def __init__(self, input):
        super(PointSet, self).__init__()
        lines = input.split("\n")
        self.points = []
        self.data = lines[0].split(",")
        self.xcoors = lines[1].split(",")
        self.ycoors = lines[2].split(",")
        self.sol = lines[3].split(",")
        self.currgen = []
        for n in range(len(self.xcoors)):
            self.points.append(Point(self.xcoors[n], self.ycoors[n]))

    def gen1(self):
        for x in range(5):
            self.currgen.append(self.genshuffle(self.points))

    def calcfitness(self):
        self.allfitness = []
        for route in self.currgen:
            fitness = 0
            for point in range(len(route) - 1):
                dx2 = (route[point].x - route[point + 1].x)**2
                dy2 = (route[point].y - route[point + 1].y)**2
                dist = math.sqrt(dx2 + dy2)
                fitness += dist
            self.allfitness.append(fitness)
        # print(self.allfitness)

    def makechildren(self):
        smallestdist = min(self.allfitness)
        fittestindex = self.allfitness.index(smallestdist)
        fittest1 = self.currgen.pop(fittestindex)
        self.allfitness.pop(fittestindex)

        smallestdist = min(self.allfitness)
        fittestindex = self.allfitness.index(smallestdist)
        fittest2 = self.currgen.pop(fittestindex)
        self.allfitness.pop(fittestindex)

        # print(fittest1, fittest2)


        trindex = random.sample(range(len(fittest1)), 2)
        trindex.sort()
        # print(fittest1[trindex[0]:trindex[1]])
        child = []
        for x in range(len(fittest1)):
            child.append(0)
        child[trindex[0]:trindex[1]] = fittest1[trindex[0]:trindex[1]]
        for n, element in enumerate(fittest2):
            for c in child:
                if c != 0:
                    if element.x == c.x and element.y == c.y:
                        fittest2[n] = 0
        # for n, x in enumerate(child):
        #     if x == 0:
        #         # child[n] = fittest2[n]
        #         for y in child:
        #

        print(child)
        print(fittest2)

        ccounter = trindex[1]
        fcounter = trindex[1]
        while 0 in child:
            if child[ccounter] == 0:
                if fittest2[fcounter] != 0:
                    child[ccounter] = fittest2[fcounter]
                    ccounter += 1
                    fcounter += 1
                    if fcounter == len(fittest2):
                        fcounter = 0
                    if ccounter == len(fittest2):
                        ccounter = 0
                else:
                    fcounter += 1
                    if fcounter == len(fittest2):
                        fcounter = 0
            else:
                ccounter += 1
                if ccounter == len(fittest2):
                    ccounter = 0

        print(child)

    def genshuffle(self, array):
        out = []
        random.shuffle(array)
        for x in array:
            out.append(x)
        return out

allin = open("points.csv", "r").read().split("\n\n")
allboards = {}
for x in allin[:-1]:
    allboards[x.split("\n")[0].split(",")[0]] = x

for x in allboards.keys():
    allboards[x] = PointSet(allboards[x])

# print(allboards["A12"].points)
currboard = allboards["A8"]
currboard.gen1()
currboard.calcfitness()
currboard.makechildren()

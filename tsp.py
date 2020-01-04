import random
import math


# Made by Moududur Rahman
# Shot One at a Genetic TSP Solver
# change the desired board via the BOARD variable
# all availible boards inside the points.csv
#
# ===============
# points.csv
# ===============
# boardname, bestpath
# x0,x1,x2,x3,x4,x5
# y0,y1,y2,y3,y4,y5
# sol0,sol1,sol2,sol3,sol4,sol5
#


BOARD = "A8"
POPULATION = 100
GENERATIONS = 100

class Point(object):
    """docstring for Point."""

    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return "( {} , {} )".format(self.x, self.y)


class GeneticTSP(object):
    """Describes one input"""

    def __init__(self, input):
        super(GeneticTSP, self).__init__()
        lines = input.split("\n")
        self.points = []
        self.data = lines[0].split(",")
        self.xcoors = lines[1].split(",")
        self.ycoors = lines[2].split(",")
        self.sol = lines[3].split(",")
        self.currgen = []
        self.allfitness=[]
        self.population = POPULATION
        self.orderings = {}

        for n in range(len(self.xcoors)):
            self.orderings["" + self.xcoors[n] +", "+ self.ycoors[n]] = n
            self.points.append(Point(self.xcoors[n], self.ycoors[n]))


    # intializes this generation with random solutions
    def gen1(self):
        for x in range(self.population):
            self.currgen.append(self.genshuffle(self.points))



    # updates the internal allfitness array
    # allfitness[n] corresponds with currgen[n]
    def calcfitness(self):
        self.allfitness.clear()
        for route in self.currgen:
            fitness = 0
            for point in range(len(route) - 1):
                dx2 = (route[point].x - route[point + 1].x)**2
                dy2 = (route[point].y - route[point + 1].y)**2
                dist = math.sqrt(dx2 + dy2)
                fitness += dist
            dx2 = (route[-1].x - route[0].x)**2
            dy2 = (route[-1].y - route[0].y)**2
            dist = math.sqrt(dx2 + dy2)
            fitness += dist
            self.allfitness.append(fitness)

    def makechildren(self):

        # identify the most fit members of the generation
        # store them in fittest1 and fittest2
        smallestdist = min(self.allfitness)
        fittestindex = self.allfitness.index(smallestdist)
        fittest1 = self.currgen.pop(fittestindex)
        self.allfitness.pop(fittestindex)


        smallestdist = min(self.allfitness)
        fittestindex = self.allfitness.index(smallestdist)
        fittest2 = self.currgen.pop(fittestindex)
        self.allfitness.pop(fittestindex)

        # append new childs to newgen, will be copied into and replace currgen
        newgen = []

        for m in range(self.population):
            # print("TIME TO MAKE SOME BABIES")
            fittest1c = []
            fittest2c = []

            # copies over the fittest1 and fittest2 so that they remain constant between children
            for n in range(len(fittest1)):
                fittest1c.append(Point(fittest1[n].x, fittest1[n].y))

            for n in range(len(fittest2)):
                fittest2c.append(Point(fittest2[n].x, fittest2[n].y))

            # generates 2 random numbers that fall within the range of fittest1c
            # take that subset of fittest1c, and copy it over to child
            trindex = random.sample(range(len(fittest1c)), 2)
            trindex.sort()
            child = []
            for x in range(len(fittest1c)):
                child.append(0)            # intializes child with zero's
                                           # zero's will be used as a placeholder for to be filled or empty slots
            child[trindex[0]:trindex[1]] = fittest1c[trindex[0]:trindex[1]]      # copying to child

            # all matching elements between child and fittest2 are removed from fittest2c
            # in preparation for the remaining crossover
            for n, element in enumerate(fittest2c):
                for c in child:
                    if c != 0:
                        if element.x == c.x and element.y == c.y:
                            fittest2c[n] = 0
            # print("child recieving a splice of: ", fittest1c[trindex[0]:trindex[1]])
            # print("child is now: ", child)
            # for n, x in enumerate(child):
            #     if x == 0:
            #         # child[n] = fittest2c[n]
            #         for y in child:
            #

            # start from where the fittest1c splicing finished
            # copy the remaining elements of fittest2c (non-zero) into child
            ccounter = trindex[1]
            fcounter = trindex[1]
            # print("crossover from: ", fittest2c)
            while 0 in child:
                if fcounter == len(fittest2c):
                    fcounter = 0
                if ccounter == len(fittest2c):
                    ccounter = 0

                if child[ccounter] == 0:
                    if fittest2c[fcounter] != 0:
                        child[ccounter] = fittest2c[fcounter]
                        fittest2c[fcounter] = 0
                        ccounter += 1
                        fcounter += 1
                    else:
                        fcounter += 1
                else:
                    ccounter += 1
            # print("final child: ", child)


            # mutation time baby
            # same point subset method as the slicing operation
            trindex = random.sample(range(len(child)), 2)
            if random.randint(0, 100) < 7:
                c = child[trindex[0]]
                child[trindex[0]] = child[trindex[1]]
                child[trindex[1]] = c

            # proper child made with information from both parents
            # append to newgen
            newgen.append(child)

        # copy over the newgen into the currgen
        self.currgen = newgen

    def genshuffle(self, array):
        out = []
        random.shuffle(array)
        for x in array:
            out.append(x)
        return out


#
# csv processing stuff
#
allin = open("points.csv", "r").read().split("\n\n")
allboards = {}
for x in allin:
    allboards[x.split("\n")[0].split(",")[0]] = x

for x in allboards.keys():
    allboards[x] = GeneticTSP(allboards[x])

currboard = allboards[BOARD]
currboard.gen1()


#
#the loop to handle... it's rather self-explanatory
#

for gen in range(GENERATIONS):
    currboard.calcfitness()
    currboard.makechildren()



print("THE FITTEST PATH GENERATED")
print(currboard.currgen[currboard.allfitness.index(min(currboard.allfitness))])

print()
print("ditance: ", min(currboard.allfitness))
out = []
for point in currboard.currgen[currboard.allfitness.index(min(currboard.allfitness))]:
    p = "" + str(point.x) + ", " + str(point.y)
    out.append(str(currboard.orderings[p]))

nout = []
nout.extend(out[out.index("0"):])
nout.extend(out[:out.index("0")])

nouts = ""
for x in nout:
    nouts = nouts + x + ","

print()
print("formatted path")
print(nouts)

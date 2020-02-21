from random import randint
from PIL import Image
import itertools
import time

class Voronoi:

    def populateSeedPoints(self):
        while (len(self.seedPoints) < self.numSeedPoints):
            pt = (randint(0, self.width - 1), randint(0, self.height - 1))
            if pt in self.seedPoints:
                continue
            color = ()
            for i in range(3):
                color = color + ((randint(self.colorRanges[i][0], self.colorRanges[i][1])),)
            self.seedPoints[pt] = color
        print('populated seed points')

    def __init__(self, width=1024, height=768, seedColor=-1, numSeedPoints=75, seedScale=0.15, seedPoints=None):
        """

        :type height: int
        """
        if seedPoints is None:
            seedPoints = {}
        self.width=width
        self.height=height
        self.numSeedPoints=numSeedPoints
        self.seedPoints=seedPoints

        if seedColor < 0:
            self.seedColor = (randint(0, 255), randint(0, 255), randint(0, 255))
        else:
            self.seedColor = seedColor
        if seedScale > 1.0 or seedScale < 0:
            raise RuntimeError('seedScale must be between 0 and 1')
        self.seedScale=seedScale

        self.colorRanges = ()
        for i in range(3):
            self.colorRanges = self.colorRanges + (
            (self.seedColor[i] - round(self.seedColor[i] * self.seedScale), min(self.seedColor[i] + round(self.seedColor[i] * self.seedScale), 255)),)
        print('found color ranges')

        if len(seedPoints<1):
            self.populateSeedPoints()

        self.px = [[(0,0,0) for x in range(width)] for y in range(height)]


    def pxDebug(self):
        pStr=''
        for h in range(len(self.px)):
            for w in range(len(self.px[0])):
                if((w,h) in self.seedPoints):
                    print('c',end='')
                elif(self.px[h][w]==(0,0,0)):
                    print('0',end='')
                else:
                    print('*',end='')
            print()

    #returns ((x1,y1),(x2,y2),(x3,y3)) closest seed points for a given (x,y) pt
    def getClosestPoint(self,pt):
        min=(0,0)
        minDist = float('inf')
        for i in self.seedPoints:
            dist = round(((i[0]-pt[0])**2+(i[1]-pt[1])**2)**0.5)
            if dist<minDist:
                min = i
                minDist = dist
        return min

    #for a ((x1,y1)..(xn,yn)) tuple, get the average color of all points in the seedPoints dictionary
    def getAverageColor(self,pts):
        av = [0,0,0]
        for c in pts:
            for i in range(3):
                av[i] = av[i]+round(self.seedPoints[c][i]/len(pts))
        return tuple(av)

    def naive(self):
        start = time.time()
        #pxDebug()
        for h in range(self.height):
            for w in range(self.width):
                if (w,h) in self.seedPoints:
                    self.px[h][w]= self.seedPoints[(w, h)]
                else:
                    self.px[h][w]= self.seedPoints[self.getClosestPoint((w, h))]
            if h%100==0:
                print('{0} pixel rows processed'.format(h))

        im = Image.new('RGB', (self.width, self.height))
        seq = list(itertools.chain.from_iterable(self.px))
        im.putdata(seq)
        im.show()
        print('run time: {0}'.format(time.time()-start))
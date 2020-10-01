from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # Hulls are just a list of points
    def most_right(self, points):
        largestIndex = 0
        biggest_x = points[0].x()
        for i in range(len(points)):
            if biggest_x < points[i].x():
                biggest_x = points[i].x()
                largestIndex = i
        return largestIndex

    def findUpperTangeant(self, leftHull, rightHull):
        # start with right most
        leftIndex = self.most_right(leftHull)#max(leftHull, key=leftHull.x())
        rightIndex = 0
        while True:
            firstSlope = leftHull[leftIndex].y() - rightHull[rightIndex].y() / leftHull[leftIndex].x() - rightHull[
                rightIndex].x()
            tempRightIndex = rightIndex + 1
            if tempRightIndex == len(rightHull):
                tempRightIndex = 0
            secSlope = leftHull[leftIndex].y() - rightHull[tempRightIndex].y() / leftHull[leftIndex].x() - rightHull[
                tempRightIndex].x()
            if abs(firstSlope) > abs(secSlope):  # Found the tallest slope from left most point
                break
            rightIndex += 1
            if rightIndex == len(rightHull):
                rightIndex = 0
        # upperTangeantRight = rightHull(rightIndex)
        # Find left hand side now
        while True:
            firstSlope = leftHull[leftIndex].y() - rightHull[rightIndex].y() / leftHull[leftIndex].x() - rightHull[
                rightIndex].x()
            tempLeftIndex = leftIndex - 1
            if tempLeftIndex == -1:
                tempLeftIndex = len(leftHull) - 1
            secSlope = leftHull[tempLeftIndex].y() - rightHull[rightIndex].y() / leftHull[tempLeftIndex].x() - \
                       rightHull[rightIndex].x()
            if secSlope > firstSlope:
                break
            leftIndex -= 1
            if leftIndex == -1:
                leftIndex = len(leftHull) - 1
        return [leftIndex, rightIndex]

    def findLowerTangeant(self, leftHull, rightHull):
        leftIndex = self.most_right(leftHull)
        rightIndex = 0
        while True:
            firstSlope = leftHull[leftIndex].y() - rightHull[rightIndex].y() / leftHull[leftIndex].x() - rightHull[
                rightIndex].x()
            tempRightIndex = rightIndex - 1
            tempTemp = len(rightHull)
            if tempRightIndex == -1:
                tempRightIndex = len(rightHull) - 1
            secSlope = leftHull[leftIndex].y() - rightHull[tempRightIndex].y() / leftHull[leftIndex].x() - rightHull[
                tempRightIndex].x()
            if (abs(firstSlope) < abs(secSlope)):  # Found the tallest slope from left most point
                break
            rightIndex -= 1
            if rightIndex == -1:
                rightIndex = len(rightHull) - 1
        # lowerRight = rightHull(rightIndex)
        # Find left hand side now
        while True:
            firstSlope = leftHull[leftIndex].y() - rightHull[rightIndex].y() / leftHull[leftIndex].x() - rightHull[
                rightIndex].x()
            tempIndex = leftIndex + 1
            if tempIndex == len(leftHull):
                tempIndex = 0
            secSlope = leftHull[tempIndex].y() - rightHull[rightIndex].y() / leftHull[tempIndex].x() - rightHull[rightIndex].x()
            if secSlope > firstSlope:
                break
            leftIndex += 1
            if leftIndex == len(leftHull):
                leftIndex = 0
            # lowerLeft = leftHull(leftIndex)
        return [rightIndex, leftIndex]


    def Merge(self, leftHull, rightHull):
        hull = []
        upperLeftIndex, upperRightIndex = self.findUpperTangeant(leftHull, rightHull)
        lowerRightIndex, lowerLeftIndex = self.findLowerTangeant(leftHull, rightHull)

        #loop until I get to first var
        #find second var and keep looping
        for i in range(upperLeftIndex):
            #temp = leftHull[i]
            hull.append(leftHull[i])
        if 0 == upperLeftIndex:
            hull.append(leftHull[upperLeftIndex])
        for i in range(lowerRightIndex - upperRightIndex):
            hull.append(rightHull[i + upperRightIndex])
        if 0 == (lowerRightIndex - upperRightIndex):
            hull.append(rightHull[upperRightIndex])
            hull.append(rightHull[lowerRightIndex])
        #until I get to firstlowertan var
        #loops until I get to second, then add rest of loop
        for i in range(lowerLeftIndex, len(leftHull) - 1):
            hull.append(leftHull[i])
        if(lowerLeftIndex == len(leftHull) - 1):
            hull.append(rightHull[lowerLeftIndex])
        return hull

    def DC(self, points):
        hull = []
        if (len(points) == 1):
            return points[0]
        elif (len(points) == 2):
            return [points[0], points[1]]
        elif (len(points) == 3):
            firstSlope = points[0].y() - points[1].y() / points[0].x() - points[1].x()
            secSlope = points[0].y() - points[2].y() / points[0].x() - points[2].x()
            if firstSlope < secSlope:
                return [points[0],points[2],points[1]]
            return points
        else:
            leftPoints = points[:len(points) // 2]
            rightPoints = points[len(points) // 2:]
            hull += self.Merge(self.DC(leftPoints), self.DC(rightPoints))
        return hull

    # This method is just to sort the points for the first part, then makes the recusive call start
    def computeHulls(self, unsorted_points):
        unsorted_points.sort(key=lambda unsorted_points: unsorted_points.x())
        leftPoints = unsorted_points[:len(unsorted_points) // 2]
        rightPoints = unsorted_points[len(unsorted_points) // 2:]
        tempLeft = self.DC(leftPoints)
        tempRight = self.DC(rightPoints)
        tempPoints = self.Merge(tempLeft, tempRight)
        return tempPoints

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        t2 = time.time()
        t3 = time.time()

        listPoints = self.computeHulls(points)
        lastLine = QLineF(listPoints[len(listPoints) - 1], listPoints[0])
        polygon = [QLineF(listPoints[i], listPoints[i + 1]) for i in range(len(listPoints) - 1)]
        polygon.append(lastLine)
        # TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon,RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
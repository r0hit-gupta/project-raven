import numpy as np
import cv2
import math
import datetime
import grequests

#Video1.mp4
#Video2.wmv

filename='asd.mp4'
cap=cv2.VideoCapture(filename)

print cap.get(4)
# print cap.grab()

# --Camera-CALIBERATION--#
Distance = 0.080  # Physical Distance between Two lines in KM(Kilometers)

counter = 1;

centerPositions = []
global blobs
blobs = []

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

ret, imgFrame1Copy = cap.read()
ret, imgFrame2Copy = cap.read()
carCount = 0
carCount2 = 0
blnFirstFrame = True
fps = 0
twovehiclecount = 0
CarWidth2 = 120
CarWidth1 = 70

# --LINE 1--#
Line1 = np.zeros((2, 2), np.float32)
horizontalLine1 = 551  # Comment for Video1.mp4
# horizontalLine1=((imgFrame2Copy.shape[0])*0.35)   #Comment for Video2.wmv
Line1[0][0] = 683 # Make it zero for Video1.mp4 and 683 for Video2.wmv
Line1[0][1] = horizontalLine1
# Line1[1][0] = 998  # Comment for Video1.mp4
Line1[1][0]= imgFrame2Copy.shape[1] - 1           #Comment for Video2.wmv
Line1[1][1] = horizontalLine1

# --LINE 2--#
Line2 = np.zeros((2, 2), np.float32)
horizontalLine2 = 480  # Comment for Video1.mp4
# horizontalLine2=((imgFrame2Copy.shape[0])*0.65)   #Comment for Video2.wmv
Line2[0][0] = 683  # Make it 0 for Video1.mp4 and 683 for Video2.wmv
Line2[0][1] = horizontalLine2
Line2[1][0] = 998  # Comment for Video1.mp4
# Line2[1][0]= imgFrame2Copy.shape[1] - 1           #Comment for Video2.wmv
Line2[1][1] = horizontalLine2


def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    # print millis
    return millis


def time_diff(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    # print millis
    return millis


# define blob filter for blob analysing and filtering of bad blobs
class blobz(object):
    def __init__(self, contour):
        global currentContour
        global currentBoundingRect
        global centerPosition
        global centerPositions
        global cx
        global cy
        global speed
        global startTime
        global endTime
        global startTime1
        global endTime1
        global dblCurrentDiagonalSize
        global dblCurrentAspectRatio
        global intCurrentRectArea
        global blnCurrentMatchFoundOrNewBlob
        global blnStillBeingTracked
        global intNumOfConsecutiveFramesWithoutAMatch
        global predictedNextPosition
        global numPositions
        self.predictedNextPosition = []
        self.centerPosition = []
        currentBoundingRect = []
        currentContour = []
        self.centerPositions = []
        self.currentContour = contour
        self.currentBoundingArea = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        self.currentBoundingRect = [x, y, w, h]
        cx = (2 * x + w) / 2
        cy = (2 * y + h) / 2
        self.centerPosition = [cx, cy]
        self.dblCurrentDiagonalSize = math.sqrt(w * w + h * h)
        self.dblCurrentAspectRatio = (w / (h * 1.0))
        self.intCurrentRectArea = w * h
        self.blnStillBeingTracked = True
        self.blnCurrentMatchFoundOrNewBlob = True
        self.intNumOfConsecutiveFramesWithoutAMatch = 0
        self.centerPositions.append(self.centerPosition)

    def predictNextPosition(self):
        # next position prediction algorithm based on last 5 weighing sum of tracked blob positions
        numPositions = len(self.centerPositions)
        if (numPositions == 1):
            self.predictedNextPosition = [self.centerPositions[-1][-2], self.centerPositions[-1][-1]]
        if (numPositions == 2):
            deltaX = self.centerPositions[1][0] - self.centerPositions[0][0]
            deltaY = self.centerPositions[1][1] - self.centerPositions[0][1]
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]
        if (numPositions == 3):
            sumOfXChanges = ((self.centerPositions[2][0] - self.centerPositions[1][0]) * 2) + (
            (self.centerPositions[1][0] - self.centerPositions[0][0]) * 1)
            deltaX = (sumOfXChanges / 3)
            sumOfYChanges = ((self.centerPositions[2][1] - self.centerPositions[1][1]) * 2) + (
            (self.centerPositions[1][1] - self.centerPositions[0][1]) * 1)
            deltaY = (sumOfYChanges / 3)
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]
        if (numPositions == 4):
            sumOfXChanges = ((self.centerPositions[3][0] - self.centerPositions[2][0]) * 3) + (
            (self.centerPositions[2][0] - self.centerPositions[1][0]) * 2) + (
                            (self.centerPositions[1][0] - self.centerPositions[0][0]) * 1)
            deltaX = (sumOfXChanges / 6)
            sumOfYChanges = ((self.centerPositions[3][1] - self.centerPositions[2][1]) * 3) + (
            (self.centerPositions[2][1] - self.centerPositions[1][1]) * 2) + (
                            (self.centerPositions[1][1] - self.centerPositions[0][1]) * 1)
            deltaY = (sumOfYChanges / 6)
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]
        if (numPositions >= 5):
            sumOfXChanges = ((self.centerPositions[numPositions - 1][0] - self.centerPositions[numPositions - 2][
                0]) * 4) + ((self.centerPositions[numPositions - 2][0] - self.centerPositions[numPositions - 3][
                0]) * 3) + ((self.centerPositions[numPositions - 3][0] - self.centerPositions[numPositions - 4][
                0]) * 2) + ((self.centerPositions[numPositions - 4][0] - self.centerPositions[numPositions - 5][0]) * 1)
            sumOfYChanges = ((self.centerPositions[numPositions - 1][1] - self.centerPositions[numPositions - 2][
                1]) * 4) + ((self.centerPositions[numPositions - 2][1] - self.centerPositions[numPositions - 3][
                1]) * 3) + ((self.centerPositions[numPositions - 3][1] - self.centerPositions[numPositions - 4][
                1]) * 2) + ((self.centerPositions[numPositions - 4][1] - self.centerPositions[numPositions - 5][1]) * 1)
            deltaX = (sumOfXChanges / 10)
            deltaY = (sumOfYChanges / 10)
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]


def matchCurrentFrameBlobsToExistingBlobs(blobs, currentFrameBlobs):
    for existingBlob in blobs:
        existingBlob.blnCurrentMatchFoundOrNewBlob = False
        existingBlob.predictNextPosition()
    for currentFrameBlob in currentFrameBlobs:
        intIndexOfLeastDistance = 0
        dblLeastDistance = 1000000.0
        for i in range(len(blobs)):
            if (blobs[i].blnStillBeingTracked == True):
                dblDistance = distanceBetweenPoints(currentFrameBlob.centerPositions[-1],
                                                    blobs[i].predictedNextPosition)
                if (dblDistance < dblLeastDistance):
                    dblLeastDistance = dblDistance
                    intIndexOfLeastDistance = i

        # print range(len(blobs))
        if (dblLeastDistance < (currentFrameBlob.dblCurrentDiagonalSize * 1.0) / 1.2):
            blobs = addBlobToExistingBlobs(currentFrameBlob, blobs, intIndexOfLeastDistance)
        else:
            blobs, currentFrameBlob = addNewBlob(currentFrameBlob, blobs)
    for existingBlob in blobs:
        if (existingBlob.blnCurrentMatchFoundOrNewBlob == False):
            existingBlob.intNumOfConsecutiveFramesWithoutAMatch = existingBlob.intNumOfConsecutiveFramesWithoutAMatch + 1
        if (existingBlob.intNumOfConsecutiveFramesWithoutAMatch >= 3):
            existingBlob.blnStillBeingTracked = False
    return blobs


def distanceBetweenPoints(pos1, pos2):
    if (pos2 == []):
        dblDistance = math.sqrt((pos1[0]) ** 2 + (pos1[1]) ** 2)
    else:
        dblDistance = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    # print dblDistance
    return dblDistance


def addBlobToExistingBlobs(currentFrameBlob, blobs, intIndex):
    blobs[intIndex].currentContour = currentFrameBlob.currentContour
    blobs[intIndex].currentBoundingRect = currentFrameBlob.currentBoundingRect
    blobs[intIndex].centerPositions.append(currentFrameBlob.centerPositions[-1])
    blobs[intIndex].dblCurrentDiagonalSize = currentFrameBlob.dblCurrentDiagonalSize
    blobs[intIndex].dblCurrentAspectRatio = currentFrameBlob.dblCurrentAspectRatio
    blobs[intIndex].blnStillBeingTracked = True
    blobs[intIndex].blnCurrentMatchFoundOrNewBlob = True
    return blobs


def addNewBlob(currentFrameBlob, Blobs):
    currentFrameBlob.blnCurrentMatchFoundOrNewBlob = True
    blobs.append(currentFrameBlob)
    return blobs, currentFrameBlob


speed = 0
s = 0;
u = 0


# Draw Blob Information on Image#
def drawBlobInfoOnImage(blobs, m1):
    # u=u+1
    for i in range(len(blobs)):
        if (blobs[i].blnStillBeingTracked == True):
            x, y, w, h = blobs[i].currentBoundingRect
            cv2.rectangle(m1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            text = str(i);
            cv2.putText(m1, " ID-{} ".format(text),
                        (blobs[i].centerPositions[-1][-2], blobs[i].centerPositions[-1][-1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (100, 255, 10), 2)
    return m1


# Draw Car Count On Image#
def drawCarCountOnImage(carCount, twovehiclecount, m1, fps):
    initText = " Detected Car: "
    text = initText + str(carCount) + " Detected Two Vehicle: " + str(twovehiclecount) + " Frame No : " + str(
        frameNo) + " FRAME RATE: " + str(int(fps))
    return m1


def updateCounter(carCount):
    initText = " Detected Car: "
    text = str(carCount);
    cv2.putText(m1, "Traffic Status: {} ".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return m1


#####
def checkIfBlobsCrossedTheLine(blobs, horizontalLinePosition, carCount, twovehiclecount):
    atLeastOneBlobCrossedTheLine = False
    # car = False
    # Bike = False
    for blob in blobs:
        if (blob.blnStillBeingTracked == True and len(blob.centerPositions) >= 2):
            cx, cy = blob.centerPosition
            # print cx,cy
            prevFrameIndex = len(blob.centerPositions) - 2
            currFrameIndex = len(blob.centerPositions) - 1
            if (blob.centerPositions[prevFrameIndex][-1] > horizontalLinePosition and
                        blob.centerPositions[currFrameIndex][-1] <= horizontalLinePosition) and cx > 504 and cx < 998:
                x, y, w, h = blob.currentBoundingRect
                print w
                if (w > CarWidth1):
                    carCount = carCount + 1
                    # car = True
                else:
                    twovehiclecount = twovehiclecount + 1
                    # Bike = True
                atLeastOneBlobCrossedTheLine = True
    return atLeastOneBlobCrossedTheLine, carCount, twovehiclecount


#####

####
def checkIfBlobs2CrossedTheLine(blobs, horizontalLinePosition, carCount, twovehiclecount):
    atLeastOneBlobCrossedTheLine = False
    for blob in blobs:
        if (blob.blnStillBeingTracked == True and len(blob.centerPositions) >= 2):
            cx, cy = blob.centerPosition
            # print cx,cy
            prevFrameIndex = len(blob.centerPositions) - 2
            currFrameIndex = len(blob.centerPositions) - 1
            if (blob.centerPositions[prevFrameIndex][-1] > horizontalLinePosition and
                        blob.centerPositions[currFrameIndex][-1] <= horizontalLinePosition) and cx > 504 and cx < 998:
                x, y, w, h = blob.currentBoundingRect
                # print "y"
                if (w > CarWidth2):
                    carCount = carCount + 1
                    # print carCount
                else:
                    twovehiclecount = twovehiclecount + 1
                atLeastOneBlobCrossedTheLine = True
    return atLeastOneBlobCrossedTheLine, carCount, twovehiclecount


####
backsub = cv2.BackgroundSubtractorMOG()  # background subtraction to isolate moving cars
capture = cv2.VideoCapture(filename)
i = 0
minArea = 1

x = 0
y = 0  # Blob Verification
while (True):
    ret, frame = capture.read()
    fgmask = backsub.apply(frame, None, 0.01)
    erode = cv2.erode(fgmask, None, iterations=3)  # erosion to erase unwanted small contours
    moments = cv2.moments(erode, True)  # moments method applied
    area = moments['m00']
    if moments['m00'] >= minArea:
        x = int(moments['m10'] / moments['m00'])
        y = int(moments['m01'] / moments['m00'])
        if x > 40 and x < 55 and y > 50 and y < 65:  # range of line coordinates for values on left lane
            i = i + 1
            print(i)
        elif x > 102 and x < 110 and y > 105 and y < 130:  # range of line coordinatess for values on right lane
            i = i + 1
            print(i)
        print(x, y)
        cv2.putText(frame, 'Traffic Camera', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2)
        # cv2.imshow("Track", frame)
        dim = (600, 600)
        resized = cv2.resize(fgmask, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("background sub", resized)
    key = cv2.waitKey(100)
    if key == ord('q'):
        break
    startTime = datetime.datetime.now()
    # print startTime
    m1 = imgFrame1Copy
    n1 = imgFrame2Copy
    a1 = cv2.cvtColor(imgFrame1Copy, cv2.COLOR_BGR2GRAY)
    b1 = cv2.cvtColor(imgFrame2Copy, cv2.COLOR_BGR2GRAY)
    a2 = cv2.GaussianBlur(a1, (5, 5), 0)
    b2 = cv2.GaussianBlur(b1, (5, 5), 0)
    imgDifference = cv2.absdiff(b2, a2)
    ret1, th1 = cv2.threshold(imgDifference, 30, 255, cv2.THRESH_BINARY)
    th1 = cv2.dilate(th1, kernel, iterations=1)
    th1 = cv2.dilate(th1, kernel, iterations=1)
    fgmask = cv2.erode(th1, kernel, iterations=1)
    frameNo = cap.get(1)
    fgmask = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel1)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel2)
    fg2 = np.zeros((fgmask.shape[0], fgmask.shape[1], 3), np.uint8)
    fg3 = np.zeros((fgmask.shape[0], fgmask.shape[1], 3), np.uint8)
    # cv2.waitKey(20)

    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(fg2, contours, -1, (255, 255, 255), -1)
    hulls = []
    for c in range(len(contours)):
        hull = cv2.convexHull(contours[c])
        hulls.append(hull)
    curFrameblobs = []
    for c in range(len(hulls)):
        ec = blobz(hulls[c])
        if (
                                    ec.intCurrentRectArea > 100 and ec.dblCurrentAspectRatio >= 0.2 and ec.dblCurrentAspectRatio <= 1.2 and ec.dblCurrentDiagonalSize > 30 and
                        ec.currentBoundingRect[2] > 20 and ec.currentBoundingRect[3] > 20 and (
                ec.currentBoundingArea * 1.0 / ec.intCurrentRectArea) > .4):
            curFrameblobs.append(ec)

    if (blnFirstFrame == True):
        for f1 in curFrameblobs:
            blobs.append(f1)
    else:
        blobs = matchCurrentFrameBlobsToExistingBlobs(blobs, curFrameblobs)

    print len(curFrameblobs)

    # buglife
    # if (counter % 20 == 0):
    #     r = grequests.get('http://b0cb8303.ngrok.io/cars/' + str(len(curFrameblobs)))
    #     grequests.map([r])
    #     print r
    # counter = counter + 1;

    m1 = drawBlobInfoOnImage(blobs, m1)
    blob2 = blobs
    # cv2.imshow('original1',m1)
    atLeastOneBlobCrossedTheLine, carCount, twovehiclecount = checkIfBlobsCrossedTheLine(blobs, horizontalLine2,
                                                                                         carCount, twovehiclecount)
    atLeastOneBlobCrossedTheLine2, carCount2, twovehiclecount2 = checkIfBlobs2CrossedTheLine(blobs, horizontalLine1,
                                                                                             carCount2, twovehiclecount)
    if (atLeastOneBlobCrossedTheLine):
        cv2.line(m1, (Line2[0][0], Line2[0][1]), (Line2[1][0], Line2[1][1]), (0, 255, 0), 2)
        x = x + 1
        startTime1 = datetime.datetime.now()
        print "ID=" + str(x) + ": StartTime= " + str(startTime1)
        # print x

    if (atLeastOneBlobCrossedTheLine2):
        y = y + 1

        endTime1 = datetime.datetime.now()
        print "ID=" + str(y) + ": EndTime= " + str(endTime1)

    m1 = drawCarCountOnImage(carCount, twovehiclecount, m1, fps)
    endTime = datetime.datetime.now()
    millis = millis_interval(startTime, endTime)
    # print millis

    fps = (1.0 * 1000) / (millis+1)
    dim = (600, 600)
    resized = cv2.resize(m1, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('original', resized)
    cv2.waitKey(1)
    imgFrame1Copy = imgFrame2Copy
    ret, imgFrame2Copy = cap.read()
    if not ret:
        break
    blnFirstFrame = False

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
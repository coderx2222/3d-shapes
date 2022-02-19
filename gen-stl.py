#!/usr/bin/python

import sys
import uuid
import random
import logging

# for 3d scatter plot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

g_outputStlFile = ""
g_fileHandle = None
g_maxShapeSize = 10
g_baseCenterTop = []
g_baseBackLeft = []
g_baseFrontRight = []
g_numDesiredShapes = 42

#
# Contains all the output vertices as the shape is constructed,
# then it is all written at the end from this list
#
g_finalOutputFacets = []

def usage():
    print("USAGE:")
    print("  -g <gen-stl-file> [ -n <num-shapes> ] [ -s <max-shape-size> ] [ -plot ]")
    print("WHERE:")
    print("  Output STL will be written to <gen-stl-file>")
    print("  If -plot is specified it will plot the triangle points as a 3d scatter plot")
    exit(1)

def plotPoints(vertices):
    fig = plt.figure(figsize=(40,40))
    ax = fig.add_subplot(111, projection='3d')
    for v in range(0, len(vertices)):
        vertex = vertices[v]
        x_values = []
        y_values = []
        z_values = []
        for x in range (0, len(vertex)):
            # print("plotting point {0}, {1}, {2}".format(
                # vertex[x][0], vertex[x][1], vertex[x][2]))
            x_values.append(vertex[x][0])
            y_values.append(vertex[x][1])
            z_values.append(vertex[x][2])
    
        x_values.append(vertex[0][0])
        y_values.append(vertex[0][1])
        z_values.append(vertex[0][2])

        plt.plot(x_values, y_values, z_values, 'o', linestyle="--")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.show()
    
def plotBasePoints():
    global g_baseCenterTop
    global g_baseBackLeft
    global g_baseFrontRight

    fig = plt.figure(figsize=(40,40))
    ax = fig.add_subplot(111, projection='3d')

    x_values = []
    y_values = []
    z_values = []
    
    x_values.append(g_baseCenterTop[0])
    y_values.append(g_baseCenterTop[1])
    z_values.append(g_baseCenterTop[2])

    x_values.append(g_baseBackLeft[0])
    y_values.append(g_baseBackLeft[1])
    z_values.append(g_baseBackLeft[2])
    
    x_values.append(g_baseFrontRight[0])
    y_values.append(g_baseFrontRight[1])
    z_values.append(g_baseFrontRight[2])

    plt.plot(x_values, y_values, z_values, 'o', linestyle="--")
    plt.show()
    return

def writeData(textStr):
    global g_outputStlFile
    global g_fileHandle
    try:
        if g_fileHandle == None:
            g_fileHandle = open(g_outputStlFile, "w")
        g_fileHandle.write(str(textStr))
    except (Exception) as error:
        print("ERROR: failed to write file \"" + g_outputStlFile + "\"")
        print("Exception: {0}".format(error))
        sys.exit(1)
    
def writeHeader():
    writeData("solid {0}\n".format(g_outputStlFile))
    return

def writeTrailer():
    writeData("endsolid {0}\n".format(g_outputStlFile))

# facet normal 0.7071067690849304 -0.7071067690849304 2.264778694918419e-15
#   outer loop
#       vertex 6.852952480316162 5.085185527801514 7.5
#       vertex 7.5 5.732233047485352 7.5
#       vertex 11.352952003479004 9.585185050964355 12.0
#   endloop
# endfacet
def writeFacet(normal, vertices):
    writeData("facet normal {0} {1} {2}\n".format(
        normal[0],
        normal[1],
        normal[2]))
    writeData(" outer loop\n")
    for v in range (0, 3):
        x = int(vertices[v][0]) + 100
        y = int(vertices[v][1]) + 100
        z = int(vertices[v][2])
        writeData("  vertex {0} {1} {2}\n".format(x, y, z))
    writeData(" endloop\n")
    writeData("endfacet\n")
    return

def addCube(centerVertex, xSize, ySize, zSize):
    global g_finalOutputFacets
    left = centerVertex[0] - int(xSize / 2)
    right = centerVertex[0] + int(xSize / 2)
    front = centerVertex[1] + int(ySize / 2)
    back = centerVertex[1] - int(ySize / 2)
    top = centerVertex[2] + int(zSize / 2)
    bottom = centerVertex[2] - int(zSize / 2)
    logging.info("addCube center(%d, %d, %d) xSize = %d, ySize = %d, zSize = %d",
                 centerVertex[0], centerVertex[1], centerVertex[2],
                 xSize, ySize, zSize)
    vertices = [
    # bottom
        # base left triangle
        [ left, front, bottom ],
        [ right, front, bottom ],
        [ left, back, bottom ],
        # base right triangle
        [ right, front, bottom ],
        [ right, back, bottom ],
        [ left, back, bottom ],
    # top
        # top left triangle
        [ left, front, top ],
        [ right, front, top ],
        [ left, back, top ],
        # top right triangle
        [ right, front, top ],
        [ right, back, top ],
        [ left, back, top ],
    # front
        # left front triangle
        [ left, front, bottom ],
        [ right, front, bottom ],
        [ left, front, top ],
        # right front triangle
        [ right, front, bottom ],
        [ right, front, top ],
        [ left, front, top ],
    # back
        # left back triangle
        [ left, back, bottom ],
        [ right, back, bottom ],
        [ left, back, top ],
        # right back triangle
        [ right, back, bottom ],
        [ right, back, top ],
        [ left, back, top ],
    # left side
        # left back triangle
        [ left, back, top ],
        [ left, back, bottom ],
        [ left, front, bottom ],
        # left front triangle
        [ left, front, bottom ],
        [ left, front, top ],
        [ left, back, top ],
    # right side
        # right back triangle
        [ right, back, top ],
        [ right, back, bottom ],
        [ right, front, bottom ],
        # right front triangle
        [ right, front, bottom ],
        [ right, front, top ],
        [ right, back, top ]
    ]
    for i in range(0, len(vertices), 3):
        vertex = []
        vertex.append(vertices[i])
        vertex.append(vertices[i + 1])
        vertex.append(vertices[i + 2])
        g_finalOutputFacets.append(vertex)
    return

def addPyramid(basePoints, peakPoint):
    global g_finalOutputFacets
    base1 = basePoints[0]
    base2 = basePoints[1]
    base3 = basePoints[2]
    base4 = basePoints[3]

    vertices = [
        [ base1[0], base1[1], base1[2] ],
        [ base2[0], base2[1], base2[2] ],
        [ base3[0], base3[1], base3[2] ],
        #
        [ base1[0], base1[1], base1[2] ],
        [ base4[0], base4[1], base4[2] ],
        [ base3[0], base3[1], base3[2] ],
        #
        [ base1[0], base1[1], base1[2] ],
        [ base2[0], base2[1], base2[2] ],
        [ peakPoint[0], peakPoint[1], peakPoint[2] ],
        #
        [ base2[0], base2[1], base2[2] ],
        [ base3[0], base3[1], base3[2] ],
        [ peakPoint[0], peakPoint[1], peakPoint[2] ],
        #
        [ base3[0], base3[1], base3[2] ],
        [ base4[0], base4[1], base4[2] ],
        [ peakPoint[0], peakPoint[1], peakPoint[2] ],
        #
        [ base1[0], base1[1], base1[2] ],
        [ base4[0], base4[1], base4[2] ],
        [ peakPoint[0], peakPoint[1], peakPoint[2] ]
    ]
    for i in range(0, len(vertices), 3):
        facet = []
        facet.append(vertices[i])
        facet.append(vertices[i + 1])
        facet.append(vertices[i + 2])
        g_finalOutputFacets.append(facet)
    return

def addJumbleShape(connectPoint):
    global g_maxShapeSize
    global g_finalOutputFacets
    global g_baseBackLeft
    global g_baseFrontRight

    logging.info(
        "addJumbleShape connect point: {0},{1},{2}".format(
            connectPoint[0],
            connectPoint[1],
            connectPoint[2]))
    vertex = []
    bottom = connectPoint[2]
    upTop = connectPoint[2] + random.randint(2, g_maxShapeSize)
    vertices = []
    
    newSmallX = getNewBoundedPointVal(
        g_baseBackLeft[0] + 1, # xStart
        connectPoint[0] - 1, # xEnd
        g_baseBackLeft[0]) # default
    
    newSmallY = getNewBoundedPointVal(
        g_baseFrontRight[1] + 1, # yStart
        connectPoint[1] - 1, # yEnd
        g_baseFrontRight[1]) # default
    
    newBigX = getNewBoundedPointVal(
        connectPoint[0] + 1, # xStart
        g_baseFrontRight[0] - 1, # xEnd
        g_baseFrontRight[0]) # default
    
    newBigY = getNewBoundedPointVal(
        connectPoint[1] + 1, # yStart
        g_baseBackLeft[1] - 1, # yEnd
        g_baseBackLeft[1]) # default

    #
    # Use the new points
    #
    if True:
        point = [ newSmallX, newSmallY, bottom ]
        vertex.append(point)
        #
        point = [ newBigX, newSmallY, bottom ]
        vertex.append(point)
        #
        point = [ connectPoint[0], newBigY, bottom ]
        vertex.append(point)
        vertices.append(vertex)
    if True:
        vertex = []
        point = [ newSmallX, newSmallY, upTop ]
        vertex.append(point)
        #
        point = [ newBigX, newSmallY, upTop ]
        vertex.append(point)
        #
        point = [ connectPoint[0], newBigY, upTop ]
        vertex.append(point)
        vertices.append(vertex)
    if True:
        vertex = []
        point = [ newSmallX, newSmallY, bottom ]
        vertex.append(point)
        #
        point = [ connectPoint[0], newSmallY, bottom ]
        vertex.append(point)
        #
        point = [ newSmallX, newSmallY, upTop ]
        vertex.append(point)
        vertices.append(vertex)
    if True:
        vertex = []
        point = [ connectPoint[0], newSmallY, bottom ]
        vertex.append(point)
        #
        point = [ newBigX, newSmallY, bottom ]
        vertex.append(point)
        #
        point = [ newBigX , newSmallY, upTop ]
        vertex.append(point)
        vertices.append(vertex)
    if True:
        vertex = []
        point = [ newSmallX, newSmallY, upTop ]
        vertex.append(point)
        #
        point = [ newBigX, newSmallY, upTop ]
        vertex.append(point)
        #
        point = [ connectPoint[0] , newSmallY, bottom ]
        vertex.append(point)
        vertices.append(vertex)
        
    # side
    if True:
        vertex = []
        point = [ newBigX, newSmallY, upTop ]
        vertex.append(point)
        #
        point = [ newBigX, newBigY, upTop ]
        vertex.append(point)
        #
        point = [ connectPoint[0] , newBigY, bottom ]
        vertex.append(point)
        vertices.append(vertex)
    if True:
        vertex = []
        point = [ newBigX, newSmallY, upTop ]
        vertex.append(point)
        #
        point = [ newBigX, newSmallY, bottom ]
        vertex.append(point)
        #
        point = [ connectPoint[0] , newBigY, upTop ]
        vertex.append(point)
        vertices.append(vertex)

        
    for counter in range(0, len(vertices)):
        g_finalOutputFacets.append(vertices[counter])
        
    return

def formBase():
    global g_maxShapeSize
    global g_baseCenterTop
    global g_baseBackLeft
    global g_baseFrontRight
    baseHeight = 2
    center = [ 0, 0, 0 ]
    addCube(center, g_maxShapeSize * 2, g_maxShapeSize * 2, baseHeight)
    halfWidth = int(g_maxShapeSize / 2)
    g_baseCenterTop = [ center[0], center[1], center[2] + int(baseHeight / 2) ]
    g_baseBackLeft = [ 0 - halfWidth, 0 + halfWidth, g_baseCenterTop[2] ]
    g_baseFrontRight = [ 0 + halfWidth, 0 - halfWidth, g_baseCenterTop[2] ]
    logging.info("base top center %d, %d, %d",
                 g_baseCenterTop[0], g_baseCenterTop[1], g_baseCenterTop[2])
    logging.info("base back left %d, %d, %d",
                 g_baseBackLeft[0], g_baseBackLeft[1], g_baseBackLeft[2])
    logging.info("base front right %d, %d, %d",
                 g_baseFrontRight[0], g_baseFrontRight[1], g_baseFrontRight[2])
    return g_baseCenterTop

#
# Gets a random point within a space
#
def getRandomConnectionPoint(xStart, xEnd, yStart, yEnd, zStart, zEnd):
    xPoint = random.randint(xStart, xEnd)
    yPoint = random.randint(yStart, yEnd)
    zPoint = random.randint(zStart, zEnd)
    outputVertex = [ xPoint, yPoint, zPoint ]
    return outputVertex

def getNewRandomX(connectPoint):
    global g_baseCenterTop
    global g_maxShapeSize
    global g_baseBackLeft
    global g_baseFrontRight
    
    newX = 0
    xSize = random.randint(2, g_maxShapeSize)
    if connectPoint[0] - int(xSize / 2) < g_baseBackLeft[0]:
        # go to the right
        newX = connectPoint[0] + int(xSize / 2)
    elif connectPoint[0] + int(xSize / 2) > g_baseFrontRight[0]:
        # go to the left
        newX = connectPoint[0] - int(xSize / 2)
    else:
        # choose at random
        if random.randint(0, 1) == 0:
            newX = connectPoint[0] + int(xSize / 2)
        else:
            newX = connectPoint[0] - int(xSize / 2)
    return newX, xSize

def getNewRandomY(connectPoint):
    global g_baseCenterTop
    global g_maxShapeSize
    global g_baseBackLeft
    global g_baseFrontRight

    newY = 0
    ySize = random.randint(2, g_maxShapeSize)
    if connectPoint[1] - int(ySize / 2) < g_baseFrontRight[1]:
        # go backward
        newY = connectPoint[1] + int(ySize / 2)
    elif connectPoint[1] + int(ySize / 2) > g_baseBackLeft[1]:
        # go forward
        newY = connectPoint[1] - int(ySize / 2)
    else:
        # choose at random
        if random.randint(0, 1) == 0:
            newY = connectPoint[1] + int(ySize / 2)
        else:
            newY = connectPoint[1] - int(ySize / 2)
    return newY, ySize

def getNewRandomZ(connectPoint):
    global g_baseCenterTop
    global g_maxShapeSize
    global g_baseBackLeft
    global g_baseFrontRight

    newZ = 0
    zSize = random.randint(2, g_maxShapeSize)
    lowerBound = g_baseBackLeft[2]
    if (connectPoint[2] - zSize) < lowerBound:
        # go up
        newZ = connectPoint[2] + int(zSize / 2)
    else:
        # choose at random
        if random.randint(0, 1) == 0:
            newZ = connectPoint[2] + int(zSize / 2)
        else:
            newZ = connectPoint[2] - int(zSize / 2)
    return newZ, zSize

#
# Gets a new random int within start/end range
# If the distance from end - start <= 0 then
# it will just return the default value (defVal)
#
def getNewBoundedPointVal(start, end, defVal):
    newVal = defVal
    if end - start > 0:
        newVal = random.randint(start, end)
    return newVal

def addRandomCube(connectPoint):
    global g_baseCenterTop
    global g_baseBackLeft
    global g_baseFrontRight
    global g_maxShapeSize

    newX, xSize = getNewRandomX(connectPoint)
    newY, ySize = getNewRandomY(connectPoint)
    newZ, zSize = getNewRandomZ(connectPoint)
    
    newCenter = [ newX, newY, newZ ]
    
    logging.info("addRandomCube newCenter[%d, %d, %d] xSize = %d, ySize = %d, zSize = %d",
        newCenter[0], newCenter[1], newCenter[2],
        xSize, ySize, zSize)
    
    addCube(newCenter, xSize, ySize, zSize)
    outputVertex = getRandomConnectionPoint(
        newCenter[0] - int(xSize / 2), newCenter[0] + int(xSize / 2),
        newCenter[1] - int(ySize / 2), newCenter[1] + int(ySize / 2),
        newCenter[2] - int(zSize / 2), newCenter[2] - int(zSize / 2)
    )
    return outputVertex

def addRandomPyramid(connectPoint):
    global g_baseCenterTop
    global g_baseBackLeft
    global g_baseFrontRight
    global g_maxShapeSize
    
    peakX, peakXSize = getNewRandomX(connectPoint)
    peakY, peakYSize = getNewRandomY(connectPoint)
    peakZ, peakZSize = getNewRandomZ(connectPoint)
    peakPoint = [ peakX, peakY, peakZ ]
    
    basePoints = []
    basePoints.append(connectPoint)
    
    newX, newXSize = getNewRandomX(connectPoint)
    newY, newYSize = getNewRandomY(connectPoint)
    newZ, newZSize = getNewRandomZ(connectPoint)

    hiX = g_baseFrontRight[0]
    hiY = g_baseBackLeft[1]
    hiZ = g_baseFrontRight[2]
    
    loX = g_baseBackLeft[0]
    loY = g_baseFrontRight[1]
    loZ = g_baseBackLeft[2]
    
    for i in range (0, 3):
        pX, newXSize = getNewRandomX(connectPoint)
        pY, newYSize = getNewRandomY(connectPoint)
        pZ, newZSize = getNewRandomZ(connectPoint)
        nextPoint = [ pX, pY, pZ ]
        basePoints.append(nextPoint)
        hiX = max(hiX, pX)
        hiY = max(hiY, pY)
        hiZ = max(hiZ, pZ)
        #
        loX = min(loX, pX)
        loY = min(loY, pY)
        loZ = min(loZ, pZ)
        
    addPyramid(basePoints, peakPoint)
    
    connectPoint = getRandomConnectionPoint(
        loX, hiX,
        loY, hiY,
        loZ, hiZ)
    return connectPoint

def connectRandomFacet(connectionFacet):
    global g_maxShapeSize
    if len(connectionFacet) < 2:
        # it's expected there would be at least two
        print("ERROR: not enough connection points\n")
        exit(1)
    #
    # The output vertex will share the two connection
    # points and one new point
    #
    newFacet = []
    newFacet.append(connectionFacet[0])
    newFacet.append(connectionFacet[1])

    newVertex = []
    newX, xSize = getNewRandomX(connectionFacet[0])
    newY, ySize = getNewRandomY(connectionFacet[0])
    newZ, zSize = getNewRandomZ(connectionFacet[0])
                                
    newVertex.append(newX)
    newVertex.append(newY)
    newVertex.append(newZ)
    newFacet.append(newVertex)
    return newFacet

#
# This function just ensures that the lowest
# level shapes connect to the base, so that the
# overall shape is not floating.
#
def connectToBase():
    global g_finalOutputFacets
    global g_baseCenterTop
    global g_maxShapeSize
    #
    # Find the lowest shapes and make them connect
    # to the base if they're not already
    #
    z = 2
    for facetIndex in range(0, len(g_finalOutputFacets)):
        facet = g_finalOutputFacets[facetIndex]
        lowestVertex = 0
        for vertexIndex in range(0, len(facet)):
            if facet[vertexIndex][z] < facet[lowestVertex][z]:
                lowestVertex = vertexIndex
        if facet[lowestVertex][z] <= g_baseCenterTop[z]:
            continue
        if facet[lowestVertex][z] - g_baseCenterTop[z] < g_maxShapeSize / 2:
            logging.info(
                "changing facet[{0}][{1}][z] {2} to {3}".format(
                    facetIndex,
                    vertexIndex,
                    facet[lowestVertex][z],
                    g_baseCenterTop[z]))
            facet[lowestVertex][z] = g_baseCenterTop[z]
    return;

def main():
    global g_finalOutputFacets
    global g_outputStlFile
    global g_fileHandle
    global g_maxShapeSize
    global g_numDesiredShapes
    doPlotPoints = False
    plotBaseBoundary = False

    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename = "logfile.log",
        filemode = "a",
        format = Log_Format, 
        level = logging.INFO)
    
    logging.info("***** STARTING UP *****")

    # parse args
    g_outputStlFile = ""
    argiter = iter(range(1, len(sys.argv)))
    for i in argiter:
        if sys.argv[i] == '-g' and ((i + 1) < len(sys.argv)):
            g_outputStlFile = sys.argv[i + 1]
            next(argiter, None)
        elif sys.argv[i] == '-n' and ((i + 1) < len(sys.argv)):
            g_numDesiredShapes = int(sys.argv[i + 1])
            next(argiter, None)
        elif sys.argv[i] == '-s' and ((i + 1) < len(sys.argv)):
            g_maxShapeSize = int(sys.argv[i + 1])
            next(argiter, None)
        elif sys.argv[i] == "-plot":
            doPlotPoints = True
        elif sys.argv[i] == "-plotBaseBoundary":
            plotBaseBoundary = True
        else:
            usage()
            
    if len(g_outputStlFile) == 0:
        print("ERROR: must supply an output file name")
        exit(1)
            
    logging.info("writing output file: {0}".format(g_outputStlFile))

    if g_numDesiredShapes == 0:
        print("ERROR: must supply a non-zero value for number of shapes")
        exit(1)
        
    if g_maxShapeSize == 0:
        print("ERROR: must supply a non-zero value for max shape size")
        exit(1)

    logging.info("num desired shapes = %d", g_numDesiredShapes)
    logging.info("max shape size: {0}".format(g_maxShapeSize))
    
    connectionPoint = formBase()

    # debug, just show base boundary points
    if plotBaseBoundary:
        plotBasePoints()
        exit(0)
    
    choiceCount = 0
    while True:
        choice = random.randint(0, 3)
        choiceCount = choiceCount + 1
        if choice == 0:
            addJumbleShape(connectionPoint)
        elif choice == 1:
            # a pyramid adds 6 facets
            connectionPoint = addRandomPyramid(connectionPoint)
        elif choice == 2:
            # a cube adds 12 facets
            connectionPoint = addRandomCube(connectionPoint)
        else:
            facetIndex = random.randint(0, len(g_finalOutputFacets) - 1)
            connectFacet = g_finalOutputFacets[facetIndex]
            logging.info("calling connectRandomFacet with connection {0}".format(connectFacet))
            newFacet = connectRandomFacet(connectFacet)
            connectionPoint = newFacet[0]
            logging.info("calling connectRandomFacet returned {0}".format(newFacet))
            g_finalOutputFacets.append(newFacet)
            
        if choiceCount >= g_numDesiredShapes:
            break
    #
    # Not setting the normal at all.
    # A lot of CAD software actually seems to just
    # ignore it anyway and use the right-hand rule.
    #
    normal = [ 0, 0, 0 ]

    # Connect more of the lower hanging shapes
    # to the base. (floating shapes do not 3d
    # print well)
    connectToBase()
    
    writeHeader()
    for fc in range(0, len(g_finalOutputFacets)):
        writeFacet(normal, g_finalOutputFacets[fc])
    writeTrailer()
    g_fileHandle.close()
    
    if doPlotPoints:
        plotPoints(g_finalOutputFacets)

if __name__ == '__main__':
    main()

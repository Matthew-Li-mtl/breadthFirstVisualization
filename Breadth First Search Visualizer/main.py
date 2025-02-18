import datetime

print("\n\n\n")
print(datetime.datetime.now())
print("\n\n\n")

import random
import json
import math
import pygame

file = open("settings.json", "r")
fileString = file.read()
settings = json.loads(fileString)
print(settings["loaded?"])
timeBetweenSteps = settings['timeBetweenSteps']

pygame.init()
screenWidth, screenHeight = settings['screenWidth'], settings['screenHeight']
screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill((127, 127, 127))
clock = pygame.time.Clock()


# Grid internal functions
gridWidth = settings['tilesPerRow']
gridHeight = settings['tilesPerColumn']
grid = []

for i in range(gridHeight):
    row = []
    for j in range(gridWidth):
        row += ["-"]
    grid += [row]


def printGrid(separator = ""):
    print(separator)
    for row in grid:
        print(''.join(row))

def printGridMultiChar(maxElementLength, charSeparator="", gridSeparator=""):
    print(gridSeparator)
    for row in grid:
        newRow = []
        for element in row:
            for i in range(maxElementLength - len(element)):
                element += " "
            newRow += [element]
        print(charSeparator.join(newRow))

def editGrid(x, y, value):
    grid[y][x] = str(value)
def getTile(x, y):
    return grid[y][x]

# Grid drawing functions
calculatedTileWidth = math.floor(screenWidth / gridWidth)
calculatedTileHeight = math.floor(screenHeight / gridHeight)
tileLength = min(calculatedTileWidth, calculatedTileHeight)

def drawTile(x, y, color, waitTime=0):
    global tileLength
    xStart = x * tileLength
    yStart = y * tileLength
    pygame.draw.rect(screen, color, pygame.Rect(xStart, yStart, tileLength, tileLength))
    pygame.time.delay(waitTime)
    pygame.display.update()
def drawTileOutline(x, y, color, thickness, waitTime=0):
    global tileLength
    xStart = x * tileLength
    yStart = y * tileLength
    pygame.draw.rect(screen, color, pygame.Rect(xStart, yStart, tileLength, tileLength), thickness)
    pygame.time.delay(waitTime)
    pygame.display.update()    
def wait(waitTime):
    pygame.time.delay(waitTime)

endColor = tuple(settings['endColor'])
startColor = tuple(settings['startColor'])

# (Randomized) Solution path generation using subpaths
startCoord = [0, 0]
currentCoord = [0, 0]

subpaths = settings['pathSubnodes']




def addSubpath():
    maxDeltaX = math.floor(gridWidth / subpaths)
    maxDeltaY = math.floor(gridHeight / subpaths)
    minDeltaX = math.ceil(0.75 * maxDeltaX)
    minDeltaY = math.ceil(0.75 * maxDeltaY)
    
    global currentCoord
    currentX = currentCoord[0]
    currentY = currentCoord[1]
    deltaX = random.randint(minDeltaX, maxDeltaX)
    deltaY = random.randint(minDeltaY, maxDeltaY)
    print(currentX, currentY, deltaX, deltaY)
    for i in range(deltaX):
        editGrid(currentX + i, currentY, "P")
    for j in range(deltaY):
        editGrid(currentX + deltaX - 1, currentY + j, "P")
    currentCoord = [currentX + deltaX - 1, currentY + deltaY - 1]

# Randomized path gen using single lines (work in progress)
directions = ["left", "up", "right", "down"]
prevDirection = directions[random.randint(0, 3)]
minStartEndDistance = settings['lineGenMinStartEndDistance']

def addLine(randFlipperOverride=False):
    global currentCoord
    global flipper
    global randFlipper
    global prevDirection
    currentX = currentCoord[0]
    currentY = currentCoord[1]
    
    choices = []
    if prevDirection == "left" or prevDirection == "right":
        choices = ["up", "down"]
    elif prevDirection == "up" or prevDirection == "down":
        choices = ["left", "right"]
    
    newDirection = choices[random.randint(0, 1)]
    
    minMultiplier = 0.5
    minTravel = 2
    
    deltaX = 0
    deltaY = 0
    
    if newDirection == "left":
        if currentX < 2:
            addLine()
        else:
            maxDeltaX = currentX
            minDeltaX = max(minTravel, math.floor(minMultiplier * maxDeltaX))
            deltaX = -1 * random.randint(minDeltaX, maxDeltaX)
            prevDirection = newDirection
    elif newDirection == "right":
        if gridWidth - currentX <= 2:
            addLine()
        else:
            maxDeltaX = (gridWidth - 1) - currentX
            minDeltaX = max(minTravel, math.floor(minMultiplier * maxDeltaX))
            deltaX = random.randint(minDeltaX, maxDeltaX)
            prevDirection = newDirection
    elif newDirection == "up":
        if currentY < 2:
            addLine()
        else:
            maxDeltaY = currentY
            minDeltaY = max(minTravel, math.floor(minMultiplier * maxDeltaY))
            deltaY = -1 * random.randint(minDeltaY, maxDeltaY)
            prevDirection = newDirection
    elif newDirection == "down":
        if gridHeight - currentY <= 2:
            addLine()
        else:
            maxDeltaY = (gridHeight - 1) - currentY
            minDeltaY = max(minTravel, math.floor(minMultiplier * maxDeltaY))
            deltaY = random.randint(minDeltaY, maxDeltaY)
            prevDirection = newDirection
    
    
    print(newDirection)
    print(currentCoord)
    print(deltaX, deltaY)
    
    xOffset = 0
    yOffset = 0
    
    if newDirection == "left" or newDirection == "right":
        startX = currentX
        xOffset = -1
        if newDirection == "left":
            startX = currentX + deltaX
            xOffset = 0
        for i in range(abs(deltaX)):
            editGrid(startX + i, currentY, "P")
        
    else:
        startY = currentY
        yOffset = -1
        if newDirection == "up":
            startY = currentY + deltaY
            yOffset = 0
        for j in range(abs(deltaY)):
            editGrid(currentX, startY + j, "P")
        
    
    printGrid()
    
    currentCoord = [currentX + deltaX + xOffset, currentY + deltaY + yOffset]

pathGen = settings['pathGen']
if pathGen == "downRight":
    subpaths = min(math.floor(min(gridWidth, gridHeight) / 3), subpaths)
    print(subpaths)
    for i in range(subpaths):
        addSubpath()
elif pathGen == "lineGen":
    for i in range(subpaths - 1):
        addLine()
    startEndDistance = 0
    while startEndDistance < minStartEndDistance:
        addLine()
        startEndDistance = abs((currentCoord[0] - startCoord[0])) + abs((currentCoord[1] - startCoord[1]))
else:
    print("Invalid pathGen parameter in JSON!")

editGrid(startCoord[0], startCoord[1], "S")
editGrid(currentCoord[0], currentCoord[1], "E")
endCoord = [currentCoord[0], currentCoord[1]]

printGrid()

# Scatter walls around the grid, leaving the solution path unharmed
obstacleDensity = settings['obstacleDensity']
wallRenderTime = settings['wallRenderTime']
wallDrawingWaitTime =  math.floor(wallRenderTime / ((gridHeight * gridWidth) * obstacleDensity))
for i in range(gridWidth):
    for j in range(gridHeight):
        if getTile(i, j) == "-":
            roll = random.random() # float between 0 and 1
            successfulRoll = roll < obstacleDensity
            if successfulRoll:
                editGrid(i, j, "W")
                drawTile(i, j, (0, 0, 0), waitTime=wallDrawingWaitTime)
        elif getTile(i, j) != "E":
            editGrid(i, j, "-")

printGrid()
wait(timeBetweenSteps)
drawTile(startCoord[0], startCoord[1], (255, 255, 255))
drawTile(endCoord[0], endCoord[1], endColor)
wait(timeBetweenSteps)

# Breadth First Search
iteration = 0
maxLayer = 0
endCoord = [-1, -1] # although defined above, the authentic algorithm 
                    # does not know where the endpoint is until it reaches it

newLayerColor = settings['newLayerColor']
expandLayerWaitTime = settings['expandLayerWaitTime']
layerCoords = {
    0: [startCoord]
}
def expandLayer(xpos, ypos, layer):
    global maxLayer
    global layerCoords
    global endCoord
    
    if layer > maxLayer:
        maxLayer = layer
    
    if layer not in layerCoords:
        layerCoords[layer] = []
    
    drawTile(xpos, ypos, startColor)
    
    xCoordsToTry = [xpos + 1, xpos - 1, xpos, xpos]
    yCoordsToTry = [ypos, ypos, ypos + 1, ypos - 1]
    validCoords = []
    for i in range(len(xCoordsToTry)):
        newx = xCoordsToTry[i]
        newy = yCoordsToTry[i]
        if newx >= 0 and newx < gridWidth and newy >= 0 and newy < gridHeight:
            validCoords += [[newx, newy]]
    for coord in validCoords:
        xCoord = coord[0]
        yCoord = coord[1]
        if getTile(xCoord, yCoord) == "-":
            layerCoords[layer] += [coord]
            editGrid(xCoord, yCoord, layer)
            
            drawTile(xCoord, yCoord, newLayerColor, expandLayerWaitTime)
        elif getTile(xCoord, yCoord) == "E":
            endCoord = coord

def tryNewLayerCoords(layer):
    global layerCoords
    
    for coord in layerCoords[layer]:
        expandLayer(coord[0], coord[1], layer + 1)

editGrid(startCoord[0], startCoord[1], "0")
layer = 0

while len(layerCoords[layer]) > 0 and endCoord == [-1, -1]:
    tryNewLayerCoords(layer)
    layer += 1

print("End coordinate found at", endCoord)
maxLayerLength = len(str(maxLayer))
printGridMultiChar(maxLayerLength, charSeparator=" ")
wait(timeBetweenSteps)

# Gradient setup for backtracking step

startR, startG, startB = startColor[0], startColor[1], startColor[2]
endR, endG, endB = endColor[0], endColor[1], endColor[2]
"""
redGradient = [startR] + [0] * (maxLayer-2) + [endR]
greenGradient = [startG] + [0] * (maxLayer - 2) + [endG]
blueGradient = [startB] + [0] * (maxLayer - 2) + [endB]
"""
numGradientColors = maxLayer + 1
redGradient = [0] * numGradientColors
greenGradient = [0] * numGradientColors
blueGradient = [0] * numGradientColors

deltaRed = endR - startR
deltaGreen = endG - startG
deltaBlue = endB - startB

for i in range(numGradientColors):
    multiplier = i / numGradientColors
    redGradient[i] = round(startR + (deltaRed * multiplier))
    greenGradient[i] = round(startG + (deltaGreen * multiplier))
    blueGradient[i] = round(startB + (deltaBlue * multiplier))

gradientColors = []
for i in range(numGradientColors):
    color = (redGradient[i], greenGradient[i], blueGradient[i])
    gradientColors += [color]

# Backtrack from discovered endpoint to find the shortest path
backtrackingTime = settings['backtrackingTime']
def descendAndMark(xpos, ypos, layer):
    editGrid(xpos, ypos, "P")
    drawTile(xpos, ypos, gradientColors[layer], waitTime=backtrackingTime)
    if layer == 0:
        drawTileOutline(xpos, ypos, endColor, math.ceil(tileLength / 10))
        return
    xCoordsToTry = [xpos + 1, xpos - 1, xpos, xpos]
    yCoordsToTry = [ypos, ypos, ypos + 1, ypos - 1]
    for i in range(len(xCoordsToTry)):
        newx = xCoordsToTry[i]
        newy = yCoordsToTry[i]
        if newx >= 0 and newx < gridWidth and newy >= 0 and newy < gridHeight:
            newTile = getTile(newx, newy)
            if newTile.isnumeric():
                newLayer = int(newTile)
                if newLayer < layer:
                    descendAndMark(newx, newy, newLayer)
                    return

descendAndMark(endCoord[0], endCoord[1], maxLayer)
editGrid(startCoord[0], startCoord[1], "S")
editGrid(endCoord[0], endCoord[1], "E")
printGridMultiChar(maxLayerLength, charSeparator=" ")

done = False
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True
    pygame.display.update()



#pygame.quit()

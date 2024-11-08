# helloCMUGraphics.py VERSION 1.0

from cmu_graphics import *
import random
import math


def distance(x1, y1, x2, y2):
    dx = x1-x2
    dy = y1-y2
    return (dx**2 + dy**2)**0.5

def findRotation(dx, dy):
    dy = -dy #negative is down
    if dy == 0:
        if dx >= 0:
            return 90
        else:
            return 270
    elif dy >= 0:
        return(int(math.degrees(math.atan(dx/dy)))%360)
    else: #when dy is negative
        return 180+int(math.degrees(math.atan(dx/dy)))
    
def rotatePoint(cx, cy, x, y, angle):
    x = x-cx
    y = y-cy
    angle = (-angle)%360 #need to account for inverted y
    a = math.radians(angle)
    return ((x*math.cos(a)+y*math.sin(a)+cx), (-x*math.sin(a)+y*math.cos(a)+cy))


class Button: 
    def __init__ (self, left, top, width, height, color):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.bottom = top + height
        self.right = left + width
        self.cx = left + width//2
        self.cy = top + height//2
        self.color = color
    def isMouseOver(self, mouseX, mouseY):
        if self.left <= mouseX <= self.left+self.width:
            if self.top <= mouseY <= self.top+self.height:
                self.color = 'cornSilk'
                return True
        self.color = 'gold'
        return False
    def drawButton(self):
        drawRect(self.left, self.top, self.width, self.height, 
                 fill = self.color, border = 'black', borderWidth = 4)

def updateButtons(app):
    cx = app.width//2
    cy = app.height//2
    app.startButton.left = cx-app.startButton.width//2
    app.startButton.top = cy-app.startButton.height//2
    app.startButton.cx = cx
    app.startButton.cy = cy

class Bee:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.rotation = 0
        self.pollen = []
        self.frameIndex = 0
        self.stepsToNextFrame = 0

    def playerOnStep(self, mouseX, mouseY):
        #process movement
        maxSpeed = 5
        acceleration = 500
        displacementX = mouseX - self.x
        displacementY = mouseY - self.y
        distance = (displacementX**2 + displacementY**2)**0.5
        self.rotation = findRotation(displacementX, displacementY)
        d = distance
        a = acceleration
        speed = (maxSpeed**2*d/a)/(maxSpeed*d/a+1)
        speed = min(speed, distance)
        if distance != 0:
            self.x += speed*(displacementX/distance)
            self.y += speed*(displacementY/distance)
        #update animation
        baseWingSpeed = 6
        self.stepsToNextFrame -= max(1, speed)
        if self.stepsToNextFrame <= 0:
            self.stepsToNextFrame = baseWingSpeed
            self.frameIndex += 1
            self.frameIndex %= 2
        #update pollen
        for flower in self.pollen:
            if flower.growth >= 1:
                self.pollen.remove(flower)

    def updateFlowers(self, flowers):
        contactDistance = 15
        for flower in flowers:
            if distance(self.x, self.y, flower.x, flower.y) <= contactDistance:
                if flower.growth != 0:
                    continue
                if flower.sex == 'male' and flower.hasPollen:
                    flower.hasPollen = False
                    self.pollen.append(flower)
                    if len(self.pollen) > 6:
                        self.pollen.pop(0)
                elif flower.sex == 'female' and findFlowerInPollen(flower.color, self.pollen) != None:
                    maleFlower = findFlowerInPollen(flower.color, self.pollen)
                    flower.growFlower()
                    maleFlower.growFlower()

    def drawPlayer(self):
        #draw stinger
        (x1, y1) = rotatePoint(self.x, self.y, self.x+2, self.y+12, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x-2, self.y+12, self.rotation)
        (x3, y3) = rotatePoint(self.x, self.y, self.x, self.y+18, self.rotation)
        drawPolygon(x1, y1, x2, y2, x3, y3)
        #draw antennae
        (x1, y1) = rotatePoint(self.x, self.y, self.x+3, self.y-10, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x+8, self.y-16, self.rotation)
        drawLine(x1, y1, x2, y2)
        (x1, y1) = rotatePoint(self.x, self.y, self.x-3, self.y-10, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x-8, self.y-16, self.rotation)
        drawLine(x1, y1, x2, y2)
        #draw body
        drawOval(self.x, self.y, 20, 25, align = 'center',
                  fill = 'gold', rotateAngle = self.rotation)
        #draw stripes
        (x1, y1) = rotatePoint(self.x, self.y, self.x-7, self.y, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x+7, self.y, self.rotation)
        drawLine(x1, y1, x2, y2)
        (x1, y1) = rotatePoint(self.x, self.y, self.x-5, self.y+6, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x+5, self.y+6, self.rotation)
        drawLine(x1, y1, x2, y2)
        #draw wings
        if self.frameIndex == 0:
            (x1, y1) = rotatePoint(self.x, self.y, self.x-10, self.y, self.rotation)
            (x2, y2) = rotatePoint(self.x, self.y, self.x+10, self.y, self.rotation)
            drawOval(x1, y1, 16, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 60)
            drawOval(x2, y2, 16, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 60)
        else: #frameIndex is 1
            (x1, y1) = rotatePoint(self.x, self.y, self.x-8, self.y, self.rotation)
            (x2, y2) = rotatePoint(self.x, self.y, self.x+8, self.y, self.rotation)
            drawOval(x1, y1, 12, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 75)
            drawOval(x2, y2, 12, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 75)
        #draw pollen
        (x1, y1) = rotatePoint(self.x, self.y, self.x-3, self.y-17, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x-10, self.y-19, self.rotation)
        (x3, y3) = rotatePoint(self.x, self.y, self.x-10, self.y-12, self.rotation)
        (x4, y4) = rotatePoint(self.x, self.y, self.x+3, self.y-17, self.rotation)
        (x5, y5) = rotatePoint(self.x, self.y, self.x+10, self.y-19, self.rotation)
        (x6, y6) = rotatePoint(self.x, self.y, self.x+10, self.y-12, self.rotation)
        L = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6)]
        for i in range(len(self.pollen)):
            (cx, cy) = L[i]
            flower = self.pollen[i]
            drawCircle(cx, cy, 2, fill = flower.color, opacity = 70)

def drawPollenInventory(app, bee):
    startCoords = (20, 20)
    centerDistance = 25
    minSize = 10
    maxSize = 20
    (x, y) = startCoords
    for i in range(len(bee.pollen)):
        color = bee.pollen[i].color
        growth = bee.pollen[i].growth
        drawCircle(x, y, minSize + (maxSize - minSize)*growth, fill = color,
                   opacity = max(0, 100*(1 - growth)))
        x += centerDistance


class AIBee:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.rotation = 0
        self.pollen = []
        self.frameIndex = 0
        self.stepsToNextFrame = 0
        self.target = (x, y)

    def playerOnStep(self, flowers):
        #process movement
        maxSpeed = 3
        minSpeed = 2
        acceleration = 500
        if findNearestFlower(self, flowers) == None:
            self.target = (self.x, self.y)
        else:
            self.target = findNearestFlower(self, flowers)
        (targetX, targetY) = self.target
        displacementX = targetX - self.x
        displacementY = targetY - self.y
        distance = (displacementX**2 + displacementY**2)**0.5
        d = distance
        a = acceleration
        speed = (maxSpeed**2*d/a)/(maxSpeed*d/a+1) 
        speed = max(minSpeed, speed)
        speed = min(speed, distance)
        if distance != 0:
            self.x += speed*(displacementX/distance)
            self.y += speed*(displacementY/distance)
            self.rotation = findRotation(displacementX, displacementY)
        #update animation
        baseWingSpeed = 6
        self.stepsToNextFrame -= max(1, speed)
        if self.stepsToNextFrame <= 0:
            self.stepsToNextFrame = baseWingSpeed
            self.frameIndex += 1
            self.frameIndex %= 2

    def updateFlowers(self, flowers):
        contactDistance = 15
        for flower in flowers:
            if distance(self.x, self.y, flower.x, flower.y) <= contactDistance:
                if flower.growth != 0:
                    continue
                if flower.sex == 'male' and flower.hasPollen:
                    #flower.growFlower()
                    flower.hasPollen = False
                    self.pollen.append(flower)
                    if len(self.pollen) > 6:
                        self.pollen.pop(0)
                elif flower.sex == 'female' and findFlowerInPollen(flower.color, self.pollen) != None:
                    maleFlower = findFlowerInPollen(flower.color, self.pollen)
                    flower.growFlower()
                    maleFlower.growFlower()
                    self.pollen.remove(maleFlower)

    def drawPlayer(self):
        #draw stinger
        (x1, y1) = rotatePoint(self.x, self.y, self.x+2, self.y+12, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x-2, self.y+12, self.rotation)
        (x3, y3) = rotatePoint(self.x, self.y, self.x, self.y+18, self.rotation)
        drawPolygon(x1, y1, x2, y2, x3, y3)
        #draw antennae
        (x1, y1) = rotatePoint(self.x, self.y, self.x+3, self.y-10, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x+8, self.y-16, self.rotation)
        drawLine(x1, y1, x2, y2)
        (x1, y1) = rotatePoint(self.x, self.y, self.x-3, self.y-10, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x-8, self.y-16, self.rotation)
        drawLine(x1, y1, x2, y2)
        #draw body
        drawOval(self.x, self.y, 20, 25, align = 'center',
                  fill = 'gold', rotateAngle = self.rotation)
        #draw stripes
        (x1, y1) = rotatePoint(self.x, self.y, self.x-7, self.y, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x+7, self.y, self.rotation)
        drawLine(x1, y1, x2, y2)
        (x1, y1) = rotatePoint(self.x, self.y, self.x-5, self.y+6, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x+5, self.y+6, self.rotation)
        drawLine(x1, y1, x2, y2)
        #draw wings
        if self.frameIndex == 0:
            (x1, y1) = rotatePoint(self.x, self.y, self.x-10, self.y, self.rotation)
            (x2, y2) = rotatePoint(self.x, self.y, self.x+10, self.y, self.rotation)
            drawOval(x1, y1, 16, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 60)
            drawOval(x2, y2, 16, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 60)
        else: #frameIndex is 1
            (x1, y1) = rotatePoint(self.x, self.y, self.x-8, self.y, self.rotation)
            (x2, y2) = rotatePoint(self.x, self.y, self.x+8, self.y, self.rotation)
            drawOval(x1, y1, 12, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 75)
            drawOval(x2, y2, 12, 10, align = 'center', rotateAngle = self.rotation,
                    fill = 'lightSteelBlue', opacity = 75)
        #draw pollen
        (x1, y1) = rotatePoint(self.x, self.y, self.x-3, self.y-17, self.rotation)
        (x2, y2) = rotatePoint(self.x, self.y, self.x-10, self.y-19, self.rotation)
        (x3, y3) = rotatePoint(self.x, self.y, self.x-10, self.y-12, self.rotation)
        (x4, y4) = rotatePoint(self.x, self.y, self.x+3, self.y-17, self.rotation)
        (x5, y5) = rotatePoint(self.x, self.y, self.x+10, self.y-19, self.rotation)
        (x6, y6) = rotatePoint(self.x, self.y, self.x+10, self.y-12, self.rotation)
        L = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6)]
        for i in range(len(self.pollen)):
            (cx, cy) = L[i]
            flower = self.pollen[i]
            drawCircle(cx, cy, 2, fill = flower.color, opacity = 70)

def findFlowerInPollen(color, pollenList):
    for flower in pollenList:
        if flower.color == color:
            return flower

def findNearestFlower(bee, flowers): 
    if flowers == []:
        return None
    nearestFlower = None
    nearestDistance = None
    for flower in flowers:
        if flower.sex == 'female':
            if findFlowerInPollen(flower.color, bee.pollen) == None:
                continue
            if flower.growth != 0:
                continue
        if flower.sex == 'male':
            if not flower.hasPollen:
                continue
            if nearestFlower != None and nearestFlower.sex == 'female':
                continue
            if len(bee.pollen) == 6:
                continue
        currDistance = distance(bee.x, bee.y, flower.x, flower.y)
        if nearestDistance == None or currDistance < nearestDistance:
            nearestFlower = flower
            nearestDistance = currDistance
    if nearestFlower == None:
        return None
    else:
        return (nearestFlower.x, nearestFlower.y)

class Flower:
    def __init__(self, x, y, color, sex, growth):
        self.x = x
        self.y = y
        self.color = color
        self.sex = sex
        self.growth = growth
        self.growSpeed = 0.05
        self.centerX = x
        self.hasPollen = True #only for males

    def growFlower(self):
        self.growth += self.growSpeed

    def flowerOnStep(self, appHeight):
        #move flower
        risingSpeed = 1
        a = 30 #sinosoidal ammplitude
        c = 0.05 #inverse sinosoidal wavelength
        self.y -= risingSpeed
        y = appHeight-self.y # bottom is 0
        self.x = self.centerX + a*math.sin(c*y)
        #grow flower
        if 0 < self.growth < 1:
            self.growth += self.growSpeed

    def drawFlower(self): 
        if self.sex == 'male':
            minSize = 15
            maxSize = 25
            if self.hasPollen:
                drawCircle(self.x, self.y, minSize, fill = self.color) #has pollen
            else:
                size = minSize + self.growth*(maxSize-minSize)
                drawCircle(self.x, self.y, size, border = self.color, 
                           borderWidth = 5, fill = None) #no pollen
        elif self.sex == 'female':
            minSize = 15
            maxSize = 25
            if self.growth == 0:
                drawCircle(self.x, self.y, minSize, border = self.color, fill = None)
                drawCircle(self.x, self.y, minSize - 5, fill = self.color) #no pollen
            else:
                size = minSize + self.growth*(maxSize-minSize)
                drawCircle(self.x, self.y, size, border = self.color, fill = None)
                drawCircle(self.x, self.y, size-5, fill = self.color) #has pollen
                
def spawnFlower(app):
    sideMargins = 10
    x = random.randrange(sideMargins, app.width-sideMargins)
    color = app.flowerColors[random.randrange(len(app.flowerColors))]
    flowerSexes = ['male', 'female']
    sex = flowerSexes[random.randrange(2)]
    app.flowers.append(Flower(x, app.height, color, sex, 0))

def removeFlowers(app, bee):
    i = 0
    while i < len(app.flowers):
        if app.flowers[i].y < 0 and app.flowers[i] not in bee.pollen:
            app.flowers.pop(i)
        else:
            i += 1


def isTutorialStageComplete(app):
    for flower in app.flowers:
        if flower.growth < 1:
            return False
    #else tutorial stage passes
    return True

def setTutorialStage(app):
    cx = app.width//2
    cy = app.height//2
    if app.gameState == 'tutorial 1':
        app.flowers = [Flower(cx+100, cy, 'cornflowerBlue', 'male', 0),
                       Flower(cx-100, cy, 'cornflowerBlue', 'female', 0)]
    if app.gameState == 'tutorial 2':
        app.flowers = [Flower(cx+100, cy+65, 'orchid', 'male', 0),
                       Flower(cx-100, cy-50, 'orchid', 'female', 0),
                       Flower(cx, cy+120, 'salmon', 'male', 0),
                       Flower(cx+30, cy-40, 'salmon', 'female', 0)]
        

def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY
    if app.gameState == 'start':
        if app.startButton.isMouseOver(mouseX, mouseY):
            pass

def onMousePress(app, mouseX, mouseY):
    if app.gameState == 'start':
        if app.startButton.isMouseOver(mouseX, mouseY):
            app.gameState = 'tutorial 1'
            setTutorialStage(app)

def onKeyPress(app, key):
    if key == 'escape': #reset game
        app.gameState = 'start'
        app.gameTimer = 0
        app.flowers = []

def onAppStart(app):
    app.gameState = 'start'
    #game states: start, tutorial1, tutorial2, tutorial3, infinite
    cx = app.width//2
    cy = app.height//2
    app.mouseX = 0
    app.mouseY = 0
    app.gameTimer = 0
    app.maxGameTime = 9999
    app.flowerTickRate = 50
    app.flowerTickVariance = 25
    app.flowerTick = 0
    app.flowerColors = ['cornflowerBlue', 'orchid', 'salmon']
    app.flowers = []
    app.bee1 = AIBee(cx-30, cy)
    app.bee2 = AIBee(cx+30, cy)
    app.player = Bee(cx, cy)
    app.startButton = Button(cx-50, cy-20, 100, 40, 'gold')

def onStep(app):
    #updateButtonCoords
    if app.gameState == 'infinite':
        app.player.playerOnStep(app.mouseX, app.mouseY)
        app.bee1.playerOnStep(app.flowers)
        app.bee2.playerOnStep(app.flowers)
        app.player.updateFlowers(app.flowers)
        app.bee1.updateFlowers(app.flowers)
        app.bee2.updateFlowers(app.flowers)
        for flower in app.flowers:
            flower.flowerOnStep(app.height)
        #generate flowers
        app.flowerTick -= 1
        if app.flowerTick <= 0:
            spawnFlower(app)
            v = app.flowerTickVariance
            app.flowerTick = app.flowerTickRate - v + random.randrange(v*2)
        removeFlowers(app, app.player)
        #update timer
        if app.gameTimer < app.maxGameTime:
            app.gameTimer += 1
    if app.gameState == 'tutorial 1':
        app.player.playerOnStep(app.mouseX, app.mouseY)
        app.player.updateFlowers(app.flowers)
        for flower in app.flowers:
            if 0 < flower.growth < 1:
                flower.growth += flower.growSpeed
        if isTutorialStageComplete(app):
            app.gameState = 'tutorial 2'
            setTutorialStage(app)
    if app.gameState == 'tutorial 2':
        app.player.playerOnStep(app.mouseX, app.mouseY)
        app.player.updateFlowers(app.flowers)
        for flower in app.flowers:
            if 0 < flower.growth < 1:
                flower.growth += flower.growSpeed
        if isTutorialStageComplete(app):
            app.flowers = []
            app.gameState = 'infinite'
    if app.gameState == 'start':
        updateButtons(app)

def redrawAll(app):
    cx = app.width//2
    cy = app.height//2
    if app.gameState == 'infinite':
        if app.gameTimer < 200:
            drawLabel('Have fun!', cx, cy-100)
            #drawLabel('You now have 2 friends', cx, cy-120)
        for flower in app.flowers:
            flower.drawFlower()
        app.player.drawPlayer()
        app.bee1.drawPlayer()
        app.bee2.drawPlayer()
        drawPollenInventory(app, app.player)
    elif app.gameState == 'tutorial 1':
        drawLabel('You are a bee!', cx, cy-120)
        drawLabel('Collect pollen from one flower to pollinate the other',
                  cx, cy-100)
        for flower in app.flowers:
            flower.drawFlower()
        app.player.drawPlayer()
        drawPollenInventory(app, app.player)
    elif app.gameState == 'tutorial 2':
        drawLabel('You can hold up to 6 pollen at a time', cx, cy-120)
        drawLabel('Different colored flowers require different pollen colors',
                  cx, cy-100)
        for flower in app.flowers:
            flower.drawFlower()
        app.player.drawPlayer()
        drawPollenInventory(app, app.player)
    elif app.gameState == 'start':
        drawLabel('BEE GAME', cx, cy-70, size = 36)
        app.startButton.drawButton()
        drawLabel('START', app.startButton.cx, app.startButton.cy,
                  font = 'orbitron', size = 16) #font doesn't work lmao
    #drawLabel(str(len(app.flowers)), cx, cy)

def main():
    runApp()

main()


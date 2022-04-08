import os
import signal
from vpython import *
import time



class GameBase():
    def __init__(self, **args) -> None:
        self.type = None
        super().__init__(**args)    
        self.vel = vec(0,0,0)  
        if "pos" not in args:
            self.pos = vec(0,0,0)  
        objects.append(self)
        self.startPos = self.pos
        
    def rem(self):
        self.visible = False

        del self

    def mouseUp(self):
        pass

    def mouseDown(self):
        pass

    def update(self):
        pass

    def reset(self):
        pass
        

class Player(GameBase, sphere):
    def __init__(self, **args) -> None:
        super().__init__(**args)    

        
    def mouseUp(self):
        if not self.canMove: return
        prelvec = self.pos-scene.mouse.pos
        self.vel=prelvec.norm()*self.force*self.charge
        self.charge = 0
        self.charging = False
        self.slowmotion = False
        
        self.canMove = False

    
    def mouseDown(self):
        if not self.canMove: return
        self.startCharge = time.time()
        self.charging = True
        self.slowmotion = True


    def update(self):
        self.charge = time.time()-self.startCharge if time.time()-self.startCharge < self.chargeTimeLimit else self.chargeTimeLimit
        chargeLabel.text = f"Charge: {self.charge/self.chargeTimeLimit*100:.0f}%"

        Trail(pos = self.pos, radius = self.radius/1.5, color = vec(0.9,0.9,0.9))


        lastCollision = None
        for obj in objects:
            if self == obj or not obj.type:
                continue
            if detectCol(obj, self):
                if lastCollision == obj:
                    continue
                if obj.type == "point":
                    normvec = norm(self.pos-obj.pos)
                    self.vel = mag(self.vel)*normvec*0.7
                    self.gainPoint()
                    obj.reset()
                    self.canMove = True

                elif obj.type == "platform":
                    self.vel = vec(0,1,0)

                lastCollision = obj
        self.lastCollision = lastCollision     
        k = keysdown()

        if not self.slowmotion:
            self.pos += self.vel
            self.vel.y -= self.gravitation 
            self.vel.x -= self.linearDrag * self.vel.x  # Linear Drag           
        else:
            self.pos += self.vel * self.slowmoAmount
            self.vel.y -= self.gravitation * self.slowmoAmount
            self.vel.x -= self.linearDrag * self.vel.x * self.slowmoAmount
    

    def gainPoint(self, amount = 1):
        self.points += amount
    

    charge = 0
    chargeTimeLimit = 1 # In seconds
    startCharge = 0
    canMove = True

    force = 7
    jumpForce = 20
    gravitation = 0.1
    linearDrag = 0 # Percent
    
    points = 0 
    type = "player"
    slowmotion = False
    slowmoAmount = 0.3
    trail = []



class Trail(GameBase, sphere):
    def __init__(self, **args):
        super().__init__(**args)
        self.startRadius = self.radius

    def update(self):
        self.radius -= self.startRadius/20
        if self.radius == 0:
            self.rem()

    

class Point(GameBase, sphere):
    def __init__(self, **args) -> None:
        super().__init__(**args)
        self.color = vec(0,1,0)
        self.radius = 7.5
        self.type = "point"
        self.reset()


    def reset(self, player = None):
        self.pos = vector.random()*300
        self.pos.z = 0




class Platform(GameBase, box):
    def __init__(self, **args):
        super().__init__(**args)
        self.type = "platform"

        if "size" in args:
            self.size = args["size"]
        else:
            self.size = vec(300,10,30)

    
    
def quitProg():
    os.kill(os.getpid(), signal.SIGTERM)


def mouseUp():
    for i in objects:
        i.mouseUp()


def mouseDown():
    for i in objects:
        i.mouseDown()    


def update():
    k = keysdown()
    for i in objects:
        i.update()
    if "esc" in k: quitProg()
    if "r" in k: reset()
    

def detectCol(obj1, obj2):
    if isinstance(obj1, sphere) and isinstance(obj2, sphere):
        objDistance = obj1.radius + obj2.radius
        if mag(obj1.pos - obj2.pos) < objDistance:
            return True
    else:
        xSize = (obj1.length + obj2.length)/2
        ySize = (obj1.height + obj2.height)/2
        zSize = (obj1.width + obj2.width)/2

        currDist = obj1.pos - obj2.pos

        xRange = abs(currDist.x) - xSize
        yRange = abs(currDist.y) - ySize
        zRange = abs(currDist.z) - zSize

        if xRange <= 0 and yRange <= 0 and zRange <= 0:
            return True


def reset():
    for i in objects:
        i.rem()
    
    start()


def start():
    global objects, player, pointList, platformList
    objects = []
    pointList = []
    platformList = []
    
    player = Player(pos=vec(0,0,0), radius = 15, color=vec(0,0,1))
    
    Platform(pos=vec(0,-150,0), color = vec(0,0,1))

    for i in range(10):
        Point()


start()

scene.width = 1400
scene.height = 700
scene.title = "xxxxxxxx"
scene.range = 240
scene.background = vec(0.1,0.1,0.1)

scene.bind("mousedown", mouseDown)
scene.bind("mouseup", mouseUp)
#scene.bind("esc", quitProg)

chargeLabel = label(pos=vec(-370,200,0), text="Charge: 0%", height=40, box = False, color = vec(1,0,0), font='sans')


while True:
    rate(60)
    update()
    
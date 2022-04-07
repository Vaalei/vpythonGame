import os
import signal
from vpython import *
import time



class GameBase(box):
    def __init__(self, **args) -> None:
        super().__init__(**args)      
        

    def update(self):
        pass

    dx = 0
    dy = 0
    speed = 0
        

class Player(GameBase):
    def __init__(self, **args) -> None:
        super().__init__(**args)        

    def update(self):
        objectLeft, objectRight, objectAbove, objectBelow = None, None, None, None
        for obj in objects:
            if self != obj:
                collision = detectCol(obj, self)
                if collision == "above" and obj != self.lastObjectAbove:
                    objectAbove = obj
                    self.isGrappling = True

                if collision == "below" and obj != self.lastObjectBelow:
                    objectBelow = obj
                    self.isGrounded = True
                if collision == "below":
                    self.pos.y += 0.2

                if collision == "left":
                    objectLeft = obj
         
                if collision == "right":
                    objectRight = obj

        if not objectBelow:
            self.isGrounded = False
        if not objectAbove:
            self.isGrappling = False

        self.lastObjectLeft = objectLeft            
        self.lastObjectRight = objectRight
        self.lastObjectAbove = objectAbove
        self.lastObjectBelow = objectBelow

        k = keysdown()
        if "a" in k:
            if self.dx > -self.speed:
                self.dx = -self.speed
        if "d" in k:
            if self.dx < self.speed:
                self.dx = self.speed
        if " " in k:
            if self.isGrappling:
                self.isGrappling = False

            elif self.isGrounded:
                self.dy = self.jumpForce
                self.isGrounded = False
        if "r" in k:
            self.pos = vec(0,0,0)
            self.dy, self.dx = 0, 0
    


        if self.dx < 0.01 and self.dx > -0.01: 
            self.dx = 0
        
        if objectLeft:
            if self.dx < 0:
                self.dx = 0
        if objectRight:
            if self.dx > 0:
                self.dx = 0


        self.pos.x += self.dx
        if self.isGrounded or self.isGrappling:
            self.grav = False
            self.dy = 0
            self.dx*=0.7            # Deaccelerates player
        else: 
            self.grav = True

        
        if self.grav == True:
            self.pos.y += self.dy
            self.dy-= self.gravitation  # Gravitational acceleration
        
        
        
    grav = True
    speed = 6
    jumpForce = 20
    gravitation = 1
    linearDrag = 0.7 # Percent
    type = "player"

    isGrounded = False

    isGrappling = False


    objectLeft, objectRight, objectAbove, objectBelow = None, None, None, None




class Platform(GameBase):
    def __init__(self, **args):
        super(GameBase, self).__init__(**args)

        objects.append(self)
        
        self.type = "platform"

        if "size" in args:
            self.size = args["size"]
        else:
            self.size = vec(300,10,30)

    
    
def quitProg():
    os.kill(os.getpid(), signal.SIGTERM)



def update():
    k = keysdown()
    if "esc" in k:
        quitProg()


    player.update()
    for i in objects:
        i.update()


def detectCol(obj1, obj2):
    xSize = (obj1.length + obj2.length)/2
    ySize = (obj1.height + obj2.height)/2
    zSize = (obj1.width + obj2.width)/2

    currDist = obj1.pos - obj2.pos

    xRange = abs(currDist.x) - xSize
    yRange = abs(currDist.y) - ySize
    zRange = abs(currDist.z) - zSize

    if xRange <= 0 and yRange <= 0 and zRange <= 0:
        if xRange > yRange and xRange > zRange:
            if currDist.x < 0:
                hitArea = "left" 
            else:
                hitArea = "right" 

        elif yRange > xRange and yRange > zRange:
            if currDist.y < 0:
                hitArea = "below" 
            else:
                hitArea = "above"

        else:
            if currDist.z < 0:
                hitArea = "front" 
            else:
                hitArea = "back"

    else:
        hitArea = False

    return hitArea



objects = []
platforms = []


player = Player(pos=vec(0,0,0), size=vec(40,40,20), color=vec(0,0,1))
platform_1 = Platform(pos=vec(0,-150,0), color=vec(0,0,1))
platform_2 = Platform(pos=vec(0,150,0), color=vec(0,0,1))
platform_3 = Platform(pos=vec(150,0,0), color=vec(0,0,1), size = vec(200, 10, 30))
wall_1 = Platform(pos=vec(-150,0,0), color=vec(0,0,1), size = vec(10,300,30))


scene.width = 1400
scene.height = 700
scene.title = "xxxxxxxx"
scene.range = 240
scene.background = vec(0.1,0.1,0.1)


continue_loop = True
while continue_loop:
    rate(60)
    update()




os.kill(os.getpid(), signal.SIGTERM)